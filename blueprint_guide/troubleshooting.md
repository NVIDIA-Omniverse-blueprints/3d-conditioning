# Troubleshooting Guide

* Cloning the Repository
   * Long file name error: You may receive an error when cloning the repository that file names are too long. To fix this issue, please try either of the following -
     * Start `Git Bash` as Administrator
     * Run command `git config --system core.longpaths true`
     * Or enable just for this cloned repository by running the command `git clone -c core.longpaths=true <repo-url>`
* Advice on long file path error on Windows when copying over files
   * Install `7zip` or some zip applications to zip the files with long path issues, then unzip in on the target directory. This is a general workaround for avoiding the issue and copy files in Windows.
* Some 'Access Denied' errors on Windows when following our instructions in a CMD can be resolved by elevating the CMD (running it on the Administrator mode).


----

| [&larr; Back to Guide](../README.md) |