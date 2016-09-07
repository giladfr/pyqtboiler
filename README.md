# pyqtboiler

PyQt application boilerplate for rapid development.
The app can be started with:
```
python baseapp/utils/hotswap.py start_app.py
```
to change code at runtime, e.g. modifying code in the draw_shapes function.
When the file mainwindow.ui is saved in QtDesigner the new window layout and controls
are also loaded into the application without the need of a restart.

Running `paver uic` translates the `.ui` files into Python code.

Running `paver buildapp` creates an executable with PyInstaller.

## License

Two files are under MIT license, the rest of the project is public domain
under the [unlicense][], see the `LICENSE` file for details.

[unlicense]: http://unlicense.org/
