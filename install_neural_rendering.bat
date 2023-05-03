git clone --recursive https://github.com/cubantonystark/neural_rendering.git
copy run_eolian.py neural_rendering\\run_eolian.py
xcopy /E /I carvekit neural_rendering\\carvekit
rmdir /S/Q carvekit
del neural_rendering\\scripts\\colmap2nerf.py
copy colmap2nerf.py /Y neural_rendering\\scripts\\colmap2nerf.py
del run_eolian.py
del colmap2nerf.py
cd neural_rendering
pip install -r requirements.txt
pip install pywin32
pip install flask
cd ..
