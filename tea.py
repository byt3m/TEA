import traceback
import sys
from t_api import *
from t_alfred import *


te = API()
al = ALFRED()
al.api = te


try:

	if len(sys.argv) > 1 and sys.argv[1] == "reloaded":
		te.SendMessage("Reload successfull.")
	else:			
		te.SendMessage("Hey, im up!\nWaiting for orders...")

	while True:
		al.received_order = te.WaitForUpdate().lower()
		al.Handler()

except SystemExit:
	pass

except KeyboardInterrupt:
	sys.exit()
	
except:
	te.ExceptionHandling(traceback.format_exc())
	al.Reload()