if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    rel_path = "tokens.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    analyzer = LexicalAnalyzer(abs_file_path)
    analyzer.analyze()
