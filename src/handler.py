from mangum import Mangum

from src.server import app

handler = Mangum(app)
