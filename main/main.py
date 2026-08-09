import requests


def wurzel(i: int) -> int:
    return i * i


def quadrat_from_api(url: str) -> int:
    response = requests.get(url)

    i = response.json().get("zahl", [])

    return i * i


def main():
    print(wurzel(2))


if __name__ == "__main__":
    main()
