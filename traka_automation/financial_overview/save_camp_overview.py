def save_camp_overview(overview, filename):
    with open(filename, "w") as f:
        for post, items in overview.items():
            f.write(f"{post}:\n")
            f.writelines(
                f"    {description}: {'' if amount >= 0 else '-'}€{abs(amount):0.2f}\n"
                for description, amount in items
            )
