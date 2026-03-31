# LiverTumorDetection

A local toolkit for liver tumor detection and classification — preprocessing, training, and a lightweight inference interface.

This repository contains scripts and models for detecting liver tumors in medical images. It includes data organization, preprocessing utilities, training scripts for object detection and classification, and a small API for inference.

## Key files
- `app.py` — web API / frontend entrypoint for inference.
- `auto_annotate.py` — helper to generate annotations automatically.
- `preprocess_dcm.py`, `preprocess_nii.py` — dataset preprocessing for DICOM / NIfTI.
- `train_yolo.py`, `train_classifier.py`, `train.py` — training scripts.
- `test_api.py` — quick API test script.
- `data/` — image and annotation dataset structure.
- `data_classifier/` — dataset used for classifier training.
- `models/` — trained model files (do not commit large binaries to git; use Git LFS or Releases).
- `requirements.txt` — Python dependencies.
- `src/` — reusable modules (predict, train, dataset, etc.).

## Quick start

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Ensure `.gitignore` excludes `venv` and large models. Example entries:

```
venv/
models/*.pth
*.pth
*.pt
__pycache__/
```

4. Run the app (example):

```powershell
python app.py
# or
python src/predict.py --image path/to/image --model models/tumor_classifier.pth
```

## Training examples

```powershell
# detection
python train_yolo.py --data data.yaml --cfg yolov8n.yaml --epochs 50

# classifier
python train_classifier.py --data data_classifier/ --epochs 30
```

Refer to `src/train.py` for full training options.

## Models and large files

Large model binaries (>100MB) cannot be pushed to GitHub normally. Options:

1) Use Git LFS:

```powershell
# install from https://git-lfs.github.com
git lfs install
git lfs track "models/*.pth"
git add .gitattributes
git add models/*.pth
git commit -m "Track model files with Git LFS"
git push
```

2) Keep model files out of the repo and provide download links or attach them to a GitHub Release.

## Cleaning history

If large files were already committed, use BFG or `git filter-repo` to remove them from history, then force-push the cleaned repo. See:
- https://rtyley.github.io/bfg-repo-cleaner/
- https://git-lfs.github.com/

## Data layout

- `data/` contains detection images and annotation text files.
- `data_classifier/` contains folders per class for classifier training.

## Contributing

1. Open an issue describing the change.
2. Fork and create a feature branch.
3. Submit a pull request.

## License

Add a license file (e.g., MIT) if desired.

## Contact

Open an issue or contact the repository owner for questions.
