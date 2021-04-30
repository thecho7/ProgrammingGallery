import sys
import random
import matplotlib.pyplot as plt
# import numpy as np
import time

A, B = list(map(int, sys.stdin.readline().rsplit()))
it = 100
results = []
for _ in range(it):
    total_size = A * A
    num_normal = total_size # 초기에 존재하는 정상 서버의 수
    threshold = 4 * num_normal // 10
    print(f"INITIAL NUMBER OF SERVERS: {num_normal}")
    print(f"SERVER THRESHOLD: {threshold}")
    NORMAL = 1
    DIE = 0

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    alives = set() # 맵을 1차원으로 보기 위한 배열
    for i in range(num_normal):
        alives.add(i)

    ######### 시작 #######
    days = 0
    # 60% 이상 무력화 되기 전까지 공격
    while num_normal > threshold:
        # 남아있는 서버가 B개가 안될 가능성도 있나?
        if num_normal < B:
            print(f"\nNumber of remaining servers {num_normal} are below B({B})")
            break

        # 만약 B개 공격하자마자 임계점을 넘는다면?
        if num_normal < 2 * B:
            num_normal -= B
            days += 1
            print(f"\nNumber of remaining servers {num_normal} are below 2B({threshold})")
            break

        # 이제 랜덤하게 B개를 공격
        attacks = random.sample(alives, B)
        for att in attacks:
            alives.remove(att)
            num_normal -= B # 공격 했으면 정상 서버 수도 줄어든다

        queue = []
        visited = set()
        clusters = [] # 클러스터의 사이즈
        for n in alives:
            if n not in visited:
                cluster = []
                queue.append(n)
                visited.add(n)
                while queue:
                    idx = queue.pop()
                    cluster.append(idx)
                    y, x = idx // A, idx % A

                    for d in directions:
                        ny, nx = y + d[0], x + d[1]
                        n_idx = ny * A + nx
                        if 0 <= ny < A and 0 <= nx < A and n_idx in alives and n_idx not in visited:
                            queue.append(n_idx)
                            visited.add(n_idx)

                clusters.append(cluster)

        sorted_clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
        max_cluster = len(sorted_clusters[0])
        candidates = [cl for cl in sorted_clusters if len(cl) == max_cluster]
        survivor = random.choice(range(len(candidates)))

        for i in range(len(sorted_clusters)):
            if i != survivor:
                for j in sorted_clusters[i]:
                    alives.remove(j)

        num_normal = len(candidates[survivor])
        days += 1

        print(f"DAY {days}: {num_normal}/{total_size} ({int(100 * num_normal / total_size)}%)")

    print(f"Elasped Days: {days} -- Simulation Completed")
    results.append(days)

average = round(float(sum(results) / len(results)), 2)
print(average)
fig = plt.figure(figsize=(10, 5))
a, b, c = plt.hist(results, bins=100, color='y', histtype='bar', edgecolor='k')
n = a.astype('int')
for i in range(len(results)):
    c[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))

plt.title(f'A: {A} - B: {B} ({it} Iterations)\nAverage: {average}')
plt.xlabel('Elasped Days', fontsize=14)
plt.ylabel('Counts', fontsize=14)
plt.tight_layout()
plt.savefig(f'{A}_{B}_stats.png')
plt.show()