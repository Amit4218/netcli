# Net-cli-server

## Net-cli-server is the heart of the application and is responsible for the server-side operations like, searching movies, extracting playable link etc, for the `Net-cli` application. The server is build using `bottle` wsgi to handel request and serve response. The server also uses `playwright`, `requests` for third-party requests and url scraping

## Pre-requisites

Before starting, ensure you have the following:

- python >= 3.10
- mpv

You might also need to install:

- [Playwright Browsers](https://playwright.dev/python/docs/intro)

---

## Features

- Able to search for a movie or series
- Movie / series identification
- playable links extraction

---

## Upcomming Features

- Cli interface
  This aims to make the server a stand-alone application, with and cli-interface,
  for users who want to just type some commands and pass flags and watch a movie, while having the features, the full application gives with the tui.

- Torrenting
  By adding this feature we wish to extend the funtionality for the application
  by letting users download torrent files, either via a magnet link provided by the user or by adding a search for the torrent.

- Video downloader
  By adding this feature we wish to enable the users to download the movies they are watching, searching. we want to also enable the users to download videos from other social media platform.

---

## Contribution

Contributions are always welcome!
If you find a bug, have an idea for a new feature, or want to improve the codebase or documentation, feel free to contribute.

### Ways to Contribute

You can help improve the project by:

- Reporting bugs
- Suggesting new features or improvements
- Improving documentation
- Fixing issues
- Submitting code improvements or optimizations

### Getting Started

1. **Fork the repository**

2. **Clone your fork**

   ```bash
   git clone https://github.com/Amit4218/netcli.git
   cd net-cli-server
   ```

3. **Create a new branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**

5. **Commit your changes**

   ```bash
   git commit -m "Add: short description of your change"
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

### Guidelines

- Keep pull requests **focused and small**
- Write **clear commit messages**
- Ensure your code follows the **existing project structure**
- Test your changes before submitting

---

### Reporting Issues

If you encounter a bug or unexpected behavior, please open an issue and include:

- A clear description of the problem
- Steps to reproduce it
- Expected vs actual behavior
- Any relevant logs or screenshots

---

### Feature Requests

Have an idea for a feature?
Start a **discussion or open an issue** describing the feature and its use case.
