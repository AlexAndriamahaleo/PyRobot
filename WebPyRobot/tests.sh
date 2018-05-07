#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    python3 manage.py test backend.tests
elif [ $# -eq 1 ] && [ $(expr "$1" : '^Test') -gt 0 ]; then
    python3 manage.py test backend.tests.$1
elif [ $# -eq 2 ] && [ $(expr "$1" : '^Test') -gt 0 ] && [ $(expr "$2" : '^test_') -gt 0 ]; then
    python3 manage.py test backend.tests.$1.$2
else
    echo -e "Usage: $0 NomClassTest [nom_methode_test]
    ¤ NomClasseTest commence par 'Test*'
    ¤ nom_méthode_test commence par 'test_*'"
fi
