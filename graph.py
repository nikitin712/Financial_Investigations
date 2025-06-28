import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch


def draw_transaction_graph(df, output_file="transactions.png"):
    plt.figure(figsize=(25, 20))
    G = nx.DiGraph()

    max_amount = df['amount'].abs().max() or 1  # Защита от деления на 0

    # Стили узлов
    styles = {
        'fiz': {'color': '#FF6B6B', 'size': 600, 'shape': 'o', 'label': 'Физлицо'},
        'OOO': {'color': 'blue', 'size': 600, 'shape': 's', 'label': 'ООО'},  # 4ECDC4
        'GUP': {'color': '#45B7D1', 'size': 600, 'shape': 'D', 'label': 'ГУП'},
        'ENT': {'color': '#FFBE0B', 'size': 600, 'shape': '^', 'label': 'ИП'},

    }

    # Добавление узлов и связей
    for _, row in df.iterrows():
        sender = row.iloc[1]
        sender_type = 'fiz' if 'fiz' in str(row['sender_body']) else 'OOO' if 'OOO' in str(row['sender_body']) \
            else 'GUP' if 'GUP' in str(row['sender_body']) else 'ENT'
        G.add_node(sender, type=sender_type)

        receiver = row.iloc[-2]
        receiver_type = 'fiz' if 'fiz' in str(row['reciever_body']) else 'OOO' if 'OOO' in str(row['reciever_body']) \
            else 'GUP' if 'GUP' in str(row['reciever_body']) else 'ENT'
        G.add_node(receiver, type=receiver_type)

        # Связь с атрибутами
        G.add_edge(sender, receiver,
                   amount=row['amount'],
                   date=row['trans_date'])

    # Позиционирование (Fruchterman-Reingold)
    pos = nx.spring_layout(G, k=0.7, iterations=100, seed=42)

    # Рисуем узлы по типам
    for typ, style in styles.items():
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[n for n, d in G.nodes(data=True) if d.get('type') == typ],
            node_shape=style['shape'],
            node_color=style['color'],
            node_size=style['size'],
            edgecolors='black',
            linewidths=1,
            alpha=0.9
        )

    # Рисуем связи
    edge_colors = []
    edge_widths = []
    for u, v, d in G.edges(data=True):
        edge_colors.append('#FF3333' if d['amount'] < 0 else '#3399FF')
        edge_width = 0.3 + (abs(d['amount']) / max_amount) * 5
        edge_widths.append(edge_width)

    nx.draw_networkx_edges(
            G, pos,
            edge_color=edge_colors,
            width=edge_widths,
            arrowsize=25,
            arrowstyle='->',
            alpha=0.7
    )

    # Подписи (имя + город)
    labels = {
        n: '\n'.join(n.split(', ')[:2])
        for n in G.nodes()
    }
    nx.draw_networkx_labels(
            G, pos,
            labels=labels,
            font_size=9,
            font_weight='bold',
            font_family='sans-serif',
            bbox=dict(
                facecolor='white',
                edgecolor='none',
                alpha=0.8,
                boxstyle='round,pad=0.3'
            )
    )

    # Легенда
    legend = [
        Patch(facecolor=s['color'], label=s['label'], edgecolor='black')
        for s in styles.values()
    ]
    plt.legend(
        handles=legend,
        loc='upper right',
        title="Типы узлов",
        fontsize=12,
        title_fontsize=14
    )

    # Заголовок с периодом
    date_range = f"{str(df['trans_date'].min()).split()[0]} — {str(df['trans_date'].max()).split()[0]}"
    plt.title(
        f"Граф транзакций между владельцами и организациями\n{date_range}",
        fontsize=18,
        pad=25
    )

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Граф сохранён как {output_file}")
    plt.show()

        # Пример вызова:
        # draw_transaction_graph(your_dataframe, "my_graph.png")