from slate_rules_notifier import create_app


def main():
    app = create_app(debug=False)
    app.run()


if __name__ == "__main__":
    main()
