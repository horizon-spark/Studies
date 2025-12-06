import pandas as pd
from itertools import combinations

class Apriori:
    def __init__(self, min_support=0.2, min_confidence=0.6):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = []
        self.frequent_itemsets = {}
        self.rules = []

    def fit(self, transactions):
        self.transactions = transactions
        self.N = len(transactions)
        
        # Находим частые наборы
        self._find_frequent_itemsets()
        # Генерируем правила
        self._generate_rules()
    
    def _support(self, itemset):
        count = sum(1 for t in self.transactions if itemset.issubset(set(t)))
        return count / self.N
    
    def _find_frequent_itemsets(self):
        # Уровень 1: отдельные элементы
        items = set(item for t in self.transactions for item in t)
        L1 = [frozenset([i]) for i in items if self._support(frozenset([i])) >= self.min_support]
        self.frequent_itemsets[1] = L1
        
        k = 2
        while self.frequent_itemsets[k-1]:
            # Генерация кандидатов
            Ck = set()
            for i in range(len(self.frequent_itemsets[k-1])):
                for j in range(i+1, len(self.frequent_itemsets[k-1])):
                    union = self.frequent_itemsets[k-1][i] | self.frequent_itemsets[k-1][j]
                    if len(union) == k:
                        Ck.add(union)
            
            # Проверка поддержки
            Lk = [c for c in Ck if self._support(c) >= self.min_support]
            if Lk:
                self.frequent_itemsets[k] = Lk
                k += 1
            else:
                break
    
    def _generate_rules(self):
        for k, itemsets in self.frequent_itemsets.items():
            if k < 2:
                continue
            for itemset in itemsets:
                items = list(itemset)
                # Генерируем все непустые подмножества
                for i in range(1, len(items)):
                    for left in combinations(items, i):
                        left_set = frozenset(left)
                        right_set = itemset - left_set
                        if right_set:
                            conf = self._support(itemset) / self._support(left_set)
                            if conf >= self.min_confidence:
                                self.rules.append((left_set, right_set, 
                                                 self._support(itemset), conf))

# Чтение данных из файла
def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    symptoms = [s.strip().lower() for s in parts[1].split(',')]
                    data.append(symptoms)
    return data

# Основная программа
def main():
    # Чтение данных
    transactions = read_data('symptoms_data.txt')
    
    # Применение алгоритма
    apriori = Apriori(min_support=0.01, min_confidence=0.35)
    apriori.fit(transactions)
    
    # Вывод результатов
    print("Частые наборы симптомов:")
    for k, itemsets in apriori.frequent_itemsets.items():
        print(f"\nНаборы из {k} симптомов:")
        for itemset in itemsets:
            supp = apriori._support(itemset)
            print(f"  {list(itemset)} - поддержка: {supp:.1%}")
    
    print("\n\nАссоциативные правила:")
    for i, (left, right, supp, conf) in enumerate(apriori.rules, 1):
        print(f"{i}. Если {list(left)} → {list(right)}")
        print(f"   Поддержка: {supp:.1%}, Достоверность: {conf:.1%}")

if __name__ == "__main__":
    main()