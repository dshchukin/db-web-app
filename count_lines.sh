cd app
find . -name '*.css' -o -name '*.html' -o -name '*.py' | xargs wc -l
cd ..
