from miniemailrelay import operations
from miniemailrelay.settings import SESSION, ENGINE
from miniemailrelay.models import Base
try:
    Base.metadata.create_all(ENGINE)
except:
    pass
sample_email = 'kesavarapu.siva@gmail.com'
operations.registerEmail(sample_email)
generated = operations.generateEmail(sample_email, "first test")
print(generated)