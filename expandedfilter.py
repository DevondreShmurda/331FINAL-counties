import webbrowser

def print_line():
    print("-" * 60)

def choose_option(prompt, options):
    print_line()
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Enter the number of your choice: ").strip()
    while not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        choice = input("Invalid input. Please choose a valid number: ").strip()
    return options[int(choice) - 1]

def usda_quickstats_helper():
    print("\n📊 USDA QUICK STATS DOWNLOAD HELPER 📊")
    print("This tool will help you figure out what filters to apply on:")
    print("https://quickstats.nass.usda.gov/")

    # Step-by-step filter selections
    program = choose_option("🔹 Select Program:", ["Census", "Survey"])

    sector = choose_option("🔹 Select Sector:", [
        "Animals & Products", "Crops", "Demographics", "Economics", "Environmental"
    ])

    group = choose_option("🔹 Select Group:", {
        "Animals & Products": ["CATTLE", "HOGS", "POULTRY"],
        "Crops": ["VEGETABLES", "GRAINS", "FRUITS", "NUTS"],
        "Demographics": ["RACE", "GENDER", "AGE"],
        "Economics": ["COMMODITY TOTALS", "AGRI-TOURISM", "PRODUCTION EXPENSES"],
        "Environmental": ["CONSERVATION PRACTICES", "IRRIGATION"]
    }[sector])

    commodity = input("🔹 Enter the commodity (e.g., CATTLE, CORN, FARMS, AGRI-TOURISM): ").upper().strip()
    category = input("🔹 Enter the category (e.g., INVENTORY, OPERATIONS, RECEIPTS): ").upper().strip()
    data_item = input("🔹 Enter the data item (copy exactly from the dropdown): ").upper().strip()
    domain = input("🔹 Enter the domain (e.g., TOTAL, BY TYPE OF OPERATION): ").upper().strip()

    geographic_level = choose_option("🔹 Geographic Level:", ["National", "State", "County", "District"])
    state = input("🔹 Enter the state (e.g., Montana): ").title().strip()
    year = input("🔹 Enter the year (e.g., 2017, 2022): ").strip()

    print_line()
    print("✅ Apply the following filters on the USDA Quick Stats site:\n")
    print(f"   • Program: {program}")
    print(f"   • Sector: {sector}")
    print(f"   • Group: {group}")
    print(f"   • Commodity: {commodity}")
    print(f"   • Category: {category}")
    print(f"   • Data Item: {data_item}")
    print(f"   • Domain: {domain}")
    print(f"   • Geographic Level: {geographic_level}")
    if geographic_level.lower() != "national":
        print(f"   • State: {state}")
    print(f"   • Year: {year}")
    print("\n4. Click 'Get Data' then 'Download' to save as CSV.")
    print(f"\n💾 Suggested file name: {state}_{commodity}_{category}_{year}.csv")
    print_line()

    # Optional browser open
    open_browser = input("🌐 Would you like to open the USDA Quick Stats site now? (yes/no): ").strip().lower()
    if open_browser in ['yes', 'y']:
        webbrowser.open("https://quickstats.nass.usda.gov/")
        print("✅ Website opened in your default browser.")
    else:
        print("📝 You can open it manually anytime at: https://quickstats.nass.usda.gov/")

# Run it
if __name__ == "__main__":
    usda_quickstats_helper()
