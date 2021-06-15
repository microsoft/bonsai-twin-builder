import sys
from app import application

twin_file = "TwinModel" if len(sys.argv) <= 1 else sys.argv[1]
application.run(twin_file)
