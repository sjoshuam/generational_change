source ~/.zshrc
conda update --all
conda create --name gcpy python=3.12 numpy=1.26 pandas=2.1 plotly=5.18 openpyxl python-kaleido -c conda-forge
echo 'alias gcpy=~/miniconda/envs/gcpy/bin/python3.12' >> ~/.zshrc
source ~/.zshrc
conda activate gcpy