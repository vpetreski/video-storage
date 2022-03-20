# Video Storage CLI

This CLI app has been built using [Typer](https://typer.tiangolo.com).

This is how you can install this command line tool in your virtual environment and use it after that.
```shell
$ poetry shell
$ poetry install
$ which video-store
```

Make sure that [backend is up and running](../README.md#backend) and then you can use it:

```shell
# Help
$ video-store --help
$ video-store upload --help
$ video-store delete --help
$ video-store download --help
$ video-store list --help

# Usage (replace PATH and ID arguments with real values)
$ video-store upload PATH
$ video-store delete ID
$ video-store download ID
$ video-store list
```

Optional improvements could be:
- Add [progress bar](https://typer.tiangolo.com/tutorial/progressbar) for upload and download operations.
- Set base API URI as environment variable

To run all the tests:

```shell
$ pytest
```

## Distribution

Python packages have a standard format called a "wheel". It's a file that ends in `.whl`. 
You can create a wheel with Poetry:

```shell
$ poetry build
```

After that, if you check in your project directory, you should now have a couple of extra files at `./dist/`.

Now anyone can open new terminal and install that package from the file for their own user with:

```shell
pip install --user dist/video_store-0.1.0-py3-none-any.whl
```

**Note:** You might need to add some user directories to the PATH.

But in the real world scenario [you would publish](https://typer.tiangolo.com/tutorial/package/#publish-to-pypi-optional) your app to PyPI to make it public, so others can install it easily.