# Site Searcher

This is a simple Flask web application that allows users to perform searches
on specified websites using DuckDuckGo and Google's `site:` search parameter. The application uses
a configuration file to specify the list of websites to search, and it
employs Selenium and Tor to circumvent anti-bot and throttling logic used
by search engines.

## Features

- Search specific websites using DuckDuckGo.
- Fallback to Google search if DuckDuckGo returns no results.
- Proxy traffic through Tor to avoid throttling and improve privacy.
- Dockerized for easy deployment.

## Prerequisites

- Docker
- Python 3.9 (if running natively)
- Google Chrome and ChromeDriver (if running natively)

## Setup

### Configuration

Create a `config.ini` file in the root directory with the following content:

```ini
[SITES]
LIST_OF_SITES = example.com, anotherexample.com
```

## Running with Docker
This is the easiest way to run the app, recommended if you just want to use it.
1. **Build the Docker Image**:
    ```sh
    docker build -t site-searcher .
    ```

2. **Run the Docker Container**:
    ```sh
    docker run -p 5000:5000 site-searcher
    ```

## Running Natively
This is what to use if you want to develop.
1. **Install the necessary Python packages** using `requirements.txt`:

   ```sh
   pip install -r requirements.txt
   ```
1. **Download ChromeDriver**: Download a ChromeDriver executable [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

1. **Set Environment Variables**:
    - Set the `CHROME_BIN` environment variable to the location the ChromeDriver was saved:
    ```sh
    export CHROME_BIN=/usr/bin/chromium
    ```

1. **Run torpy as a proxy server**
   ```sh
   torpy_socks -p 1050 --hops 3
   ```

1. **Run the Application**:
    ```sh
    python app.py
    ```

## Usage

1. Open a web browser and navigate to `http://localhost:5000`.
2. Enter search terms into the search box and submit.
3. The application will display search results from the specified websites.

## Troubleshooting

### Common Issues

- **ChromeDriver not found**: Ensure that the `chromedriver` executable is in the correct path and is executable.
- **Proxy issues**: Make sure the Tor service is running and the proxy settings are correctly configured.
  **It can take some time for Tor to establish all its streams.** Searches will fail if Tor is not successfully
  initialized. You'll know it's ready when you see the following:
  ```sh
   Start socks proxy at 127.0.0.1:1050
  ```
- **Dependency issues**: Ensure all dependencies in `requirements.txt` are installed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Acknowledgements

- [DuckDuckGo Search API](https://github.com/duckduckgo/duckduckgo-py)
- [Torpy](https://github.com/torpyorg/torpy)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
