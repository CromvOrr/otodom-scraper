import matplotlib.pyplot as plt


def show(df, df_by_district):
    df_by_district_asc = df_by_district.sort_values('qty', ascending=True)
    df_by_district_asc = df_by_district_asc.reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(df_by_district_asc['district'], df_by_district_asc['qty'], color='blueviolet')
    plt.title('Liczba ogłoszeń w poszczególnych dzielnicach')
    plt.xlabel('Dzielnica')
    plt.ylabel('Liczba ogłoszeń')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    df.hist(column='rooms', bins=13, color='blueviolet')
    plt.title('Oferty w zależności od pokojów')
    plt.xlabel('Pokoje w domu')
    plt.ylabel('Liczba ofert')
    plt.show()

    df_by_price = df.groupby('district')['price per m2 [PLN]'].mean().sort_values()
    plt.figure(figsize=(10, 6))
    df_by_price.plot(kind='barh', color='blueviolet')
    plt.title('Średnia cena za metr kwadratowy w poszczególnych dzielnicach')
    plt.xlabel('Średnia cena za metr kwadratowy [PLN]')
    plt.ylabel('Dzielnica')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.show()

    df_by_vendor_asc = df.groupby('vendor type').size().to_frame().sort_values(0, ascending=True)
    df_by_vendor_asc.columns = ['qty']
    plt.figure(figsize=(7, 6))
    plt.bar(df_by_vendor_asc.index, df_by_vendor_asc['qty'], color=['blueviolet'])
    plt.title('Oferty w zależności od sprzedawcy')
    plt.xlabel('Rodzaj sprzedawcy')
    plt.ylabel('Liczba ofert')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
