# Storage

## MongoDB

There is an option to store all output (ocean data printed to `STDOUT`). This is enabled when you specify a `DB_URI` in the `.env` file.

You can either connect to a MongoDB instance in the cloud, or locally. When using Docker, a MongoDB instance is spun up and the URI is available in the `.env.example`. 

You can view the data using multiple methods. I personally use [MongoDB Compass](https://www.mongodb.com/products/tools/compass), which is a free GUI.

