conda create -n employee_assistant python=3.11 -y
conda activate employee_assistant
pip install -r requirements.txt

如果您想从源代码安装一个包，可以通过克隆主 LangChain 仓库，进入您想安装的包的目录，然后运行：
pip install -e .

pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple

python main_admin.py
