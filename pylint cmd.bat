@echo off
copy nul pylint_log.txt
for /R %%f in (*.py) do (
	"C:\Users\secre\anaconda3\envs\py310\python.exe" -m pylint --rcfile=.pylintrc %%f >> pylint_log.txt
	echo ///////////////////////////////////////////////////////////////// >> pylint_log.txt
)