import glob
import sys
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, StratifiedKFold, GridSearchCV
from sklearn.svm import SVC, LinearSVC
from sklearn.multiclass import OneVsRestClassifier

from nibabel.funcs import concat_images
from nibabel import save
from nilearn.decoding import SearchLight
from nilearn.image import new_img_like, load_img, clean_img
from nilearn.masking import compute_brain_mask

prep_dir = '/home/data/sparse_dense/BIDS/sparseDense/derivatives/fmriprep'
betas_dir = '/home/data/sparse_dense/BIDS/sparseDense/derivatives/nibetaseries'
out_dir = '/home/data/sparse_dense/BIDS/sparseDense/derivatives/mvpa'

sub = str(sys.argv[1])
sl_radii = [4]
dim = 'sparse-dense'

def prepare_data(input_func_dir, 
                 sub,
                 dimension_list=None):
    
    combined_global = []
    labels = []
    chunks = []
    
    for run in range(1, 5):
        print(f'Load data for run-{run}')
        
        for dimension in dimension_list:
            func_runs = glob.glob(input_func_dir + f'/sub-{sub}/func/sub-{sub}_task-sparseDense_run-{run}_space-MNI152NLin2009cAsym_desc-*{dimension}*_betaseries.nii.gz')
            beta_files = []
            
            # Check if a list is empty, if it is filled: append to chunk list
            if not func_runs:
                print('>> Run is empty <<')
                continue
            
            print(func_runs)
            for betas_path in func_runs:
                img_tmp = load_img(betas_path)
                beta_files.append(img_tmp)
                    
                labels.append([str(dimension)] * img_tmp.shape[3])
                chunks.append([str(run)] * img_tmp.shape[3])
                    
                combined_img = concat_images(beta_files, axis=3)
            combined_global.append(combined_img)
    
    combined_global = concat_images(combined_global, axis=3)
    labels = np.concatenate(labels)
    chunks = np.concatenate(chunks)

    return combined_global, labels, chunks

# Use different cross-validation strategies to account for experimental design
# assign different class weights according to number of trials
if dim == 'sparse-dense':
    dimension_list=['sparse', 'dense']
    scoring = 'accuracy'
    print(f'Using scoring metric:', scoring)
    cv = KFold(n_splits=4)

    param_grid = [
    {
        'classify__C': np.logspace(-6, 2, num=5),
    },
    ]

    # Create pipeline: SVM
    svm = Pipeline([
            ('scale', StandardScaler()),
            ('svc', LinearSVC())
    ])

    # Create a gridsearch pipeline
    svm_grid = GridSearchCV(svm, param_grid,
                            return_train_score=True, refit=True, n_jobs=-1)

elif dim == 'mixed-fixed':
    dimension_list=['Mixed', 'Fixed']
    scoring = 'accuracy'
    print(f'Using scoring metric:', scoring)
    cv = KFold(n_splits=4, shuffle=True)

    # Create pipeline: SVM
    svm = Pipeline([
            ('scale', StandardScaler()),
            ('svc', SVC(kernel='rbf', gamma='auto', class_weight=None, max_iter=-1))
    ])
elif dim == 'trial-sequence':
    dimension_list=['sF', 'sD', 'dD']
    # Use appro. scoring and cross-validation method
    scoring = 'f1'
    print(f'Using scoring metric:', scoring)
    cv = StratifiedKFold(n_splits=4)

    # Create pipeline: SVM for multi-class problems
    svm = Pipeline([
            ('scale', StandardScaler()),
            ('svc', OneVsRestClassifier(SVC(kernel='rbf', gamma='auto', class_weight='balanced', max_iter=-1)))
        ])
else:
    raise ValueError('No cross-validation selected!')

tmp_ref_path = prep_dir + f'/sub-{sub}/anat/sub-{sub}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz'
brain_mask = compute_brain_mask(tmp_ref_path)

for sl_radius in sl_radii:
    # Start using different sl radii to test best fit
    chance_lvl = 1/len(dimension_list)

    # Load data, trial- and run-labels + do sanity check
    combined_global, labels, chunks = prepare_data(input_func_dir=betas_dir, sub=sub, dimension_list=dimension_list)
    if not combined_global.shape[3] == labels.shape[0] == chunks.shape[0]:
        raise ValueError('Dimensions do not add up!')

    combined_global = clean_img(imgs=combined_global, detrend=False, standardize=False, ensure_finite=True)

    sl = SearchLight(
        mask_img=brain_mask,
        process_mask_img=brain_mask,
        radius=sl_radius,
        estimator=svm, #svm_grid
        n_jobs=-1,
        scoring=scoring,
        cv=cv,
        verbose=True
    )

    # Start fitting the searchlight objects
    sl.fit(imgs=combined_global, y=labels, groups=chunks)

    score_img = new_img_like(brain_mask, sl.scores_)
    acc_path =  out_dir + f'/sl_svm/sub-{sub}_dimension-{dim}_sl-radius-{sl_radius}_smooth-0_linear-kfold.nii.gz'
    print('Saving img:', acc_path)
    save(score_img, acc_path)