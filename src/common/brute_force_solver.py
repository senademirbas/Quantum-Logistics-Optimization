import itertools

class BruteForceSolver:
    """
    Veri üretimi sırasında 'Ground Truth' (Kesin Doğru) hesaplamak için
    kullanılan yardımcı sınıf.
    """
    
    def solve(self, distance_matrix):
        """
        N < 12 için kesin çözümü bulur.
        """
        N = len(distance_matrix)
        cities = list(range(N))
        
        min_cost = float('inf')
        best_path = []
        
        # 0'ı sabitle, geri kalanı permütasyon yap (N-1)!
        for perm in itertools.permutations(cities[1:]):
            current_path = [0] + list(perm) + [0]
            
            current_cost = 0
            for i in range(N):
                u, v = current_path[i], current_path[i+1]
                current_cost += distance_matrix[u][v]
            
            if current_cost < min_cost:
                min_cost = current_cost
                best_path = current_path
                
        return best_path, min_cost