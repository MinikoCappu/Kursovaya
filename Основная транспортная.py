def inp_f(N):
    fabric = [None] * N
    string = input('Введите их производство через пробел: ').split()
    for i in range(N):
        fabric[i] = int(string[i])
    return fabric

def inp_s(N):
    shop = [None] * N
    string = input('Введите их потребление через пробел: ').split()
    for i in range(N):
        shop[i] = int(string[i])
    return shop

def cost(fac, sh):
    f = len(fac)
    s = len(sh)
    flag = False
    if sum(fac) > sum(sh):
        matrix = list()
        for i in range(f):
            arr = list(map(int, input().split()))
            arr.append(0)
            matrix.append(arr)
        flag = True
        return matrix, flag
    elif sum(fac) < sum(sh):
        matrix = list()
        for i in range(f):
            arr = list(map(int, input().split()))
            matrix.append(arr)
        matrix.append([0 for i in range(s)])
        flag = True
        return matrix, flag
    else:
        matrix = list()
        for i in range(f):
            arr = list(map(int, input().split()))
            matrix.append(arr)
        return matrix, flag
    
def fictious(fac, sh, fl):
    if fl:
        if sum(fac) > sum(sh):
            sh.append(sum(fac) - sum(sh))
        else:
            fac.append(sum(sh) - sum(fac))
    return fac, sh

def n_w_angle(fac, sh):
    iter_col = 0
    iter_row = 0
    plan = list()
    for i in range(len(fac)):
        plan.append([0 for j in range(len(sh))])
    while iter_col != len(sh) or iter_row != len(fac):
        if sh[iter_col] > fac[iter_row]:
            plan[iter_row][iter_col] = fac[iter_row]
            sh[iter_col] -= fac[iter_row]
            fac[iter_row] -= fac[iter_row] 
            iter_row += 1
        elif sh[iter_col] < fac[iter_row]:
            plan[iter_row][iter_col] = sh[iter_col]
            fac[iter_row] -= sh[iter_col] 
            sh[iter_col] -= sh[iter_col]
            iter_col += 1
        else:
            plan[iter_row][iter_col] = sh[iter_col]
            sh[iter_col] -= sh[iter_col]
            fac[iter_row] -= fac[iter_row] 
            iter_col += 1
            iter_row += 1
    return plan

def degeneracy(plan, factory, shop):
    pos_elem = 0
    for m in range(len(factory)):
        for n in range(len(shop)):
            if plan[m][n] > 0:
                pos_elem += 1
    return len(factory) + len(shop) - 1 != pos_elem

def new_degeneracy(plan):
    for m in range(len(plan)):
        for n in range(len(plan[m])):
            if plan[m][n] == 0:
                plan[m][n] = 0.001
                if not cycle_search(plan):
                    return plan
                else:
                    plan[m][n] = 0

def delete_columns(matrix, columns, rows):
    deleted = []
    for n in columns:
        non_zero = 0
        for m in rows:
            if matrix[m][n] != 0:
                non_zero += 1
                if non_zero > 1:
                    break
        if non_zero <= 1:
            deleted.append(n)
    return deleted

def cycle_search(plan):
    columns = [x for x in range(len(plan[0]))]
    rows = [x for x in range(len(plan))]
    cycle = False
    while not cycle and (len(columns) > 1 and len(rows) > 1):
        array = delete_columns(plan, columns, rows)
        if not array:
            cycle = True
        for j in array:
            columns.remove(j)
        array = delete_rows(plan, columns, rows)
        if array:
            cycle = False
        for j in array:
            rows.remove(j)
    if cycle:
        cycle_coordinates = []
        for x in rows:
            if len(cycle_coordinates) == 0:
                for y in columns:
                    if plan[x][y] != 0:
                        cycle_coordinates.append([x, y])
                        break
        while cycle_coordinates[0] != cycle_coordinates[-1] or len(cycle_coordinates) < 3:
            if len(cycle_coordinates) % 2 != 0:
                x = cycle_coordinates[-1][0]
                old_y = cycle_coordinates[-1][1]
                for y in columns:
                    if y != old_y and plan[x][y] != 0:
                        cycle_coordinates.append([x, y])
            else:
                y = cycle_coordinates[-1][1]
                old_x = cycle_coordinates[-1][0]
                for x in rows:
                    if x != old_x and plan[x][y] != 0:
                        cycle_coordinates.append([x, y])
        cycle_coordinates.pop()
        return cycle_coordinates
    
def delete_rows(matrix, columns, rows):
    deleted = []
    for m in rows:
        non_zero = 0
        for n in columns:
            if matrix[m][n] != 0:
                non_zero += 1
                if non_zero > 1:
                    break
        if non_zero <= 1:
            deleted.append(m)
    return deleted

def potential(plan, matrix):
    arr_u = [0] + [10**14 for _ in range(1, len(plan))]
    arr_v = [10**14 for _ in range(len(plan[0]))]
    while 10**14 in arr_u or 10**14 in arr_v:
        for u in range(len(arr_u)):
            if arr_u[u] != 10**14:
                for v in range(len(arr_v)):
                    if plan[u][v] != 0 and arr_v[v] == 10**14:
                        arr_v[v] = arr_u[u] + matrix[u][v]
        for v in range(len(arr_v)):
            if arr_v[v] != 10**14:
                for u in range(len(arr_u)):
                    if plan[u][v] != 0 and arr_u[u] == 10**14:
                        arr_u[u] = arr_v[v] - matrix[u][v]
    return arr_u, arr_v

def min_coord(matrix):
    idx_x = 0
    idx_y = 0
    mini = 10**14
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < mini:
                mini = matrix[i][j]
                idx_x = i
                idx_y = j
    return idx_x, idx_y

def min_elem(matrix):
    mini = 10**14
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < mini:
                mini = matrix[i][j]
    return mini

def new_matrix(plan, matrix):
    evaluation_matrix = [[n for n in matrix[m]] for m in range(len(matrix))]
    arr_u, arr_v = potential(plan, matrix)
    print('!',arr_u,arr_v)
    for m in range(len(plan)):
        for n in range(len(plan[m])):
            evaluation_matrix[m][n] = evaluation_matrix[m][n] + arr_u[m] - arr_v[n]
    print(evaluation_matrix)
    return evaluation_matrix

def next_plan(old_plan, x, y) -> list:
    old_plan[x][y] = 1
    cycle = cycle_search(old_plan)
    new_plan = [[n for n in old_plan[m]] for m in range(len(old_plan))]
    old_plan[x][y] = 0
    minus = 0
    crutch = 10**14
    for j in range(len(cycle)):
        if cycle[j][0] == x and cycle[j][1] == y:
            minus = (j - 1) % 2
            break
    for j in range(minus, len(cycle), 2):
        crutch = min(old_plan[cycle[j][0]][cycle[j][1]], crutch)
    for j in range(minus, len(cycle), 2):
        new_plan[cycle[j][0]][cycle[j][1]] = old_plan[cycle[j][0]][cycle[j][1]] - crutch
    for j in range((minus + 1) % 2, len(cycle), 2):
        new_plan[cycle[j][0]][cycle[j][1]] = old_plan[cycle[j][0]][cycle[j][1]] + crutch
    return new_plan

def answer_this(reference_plan, matrix):
    answer = 0
    for m in range(len(reference_plan)):
        for n in range(len(reference_plan[m])):
            answer += (reference_plan[m][n] * matrix[m][n])
    print(answer)
    return answer

def process():
    flag = bool
    print('Введите количество поставщиков')
    factory = inp_f(int(input()))
    print('Введите количество потребителей')
    shop = inp_s(int(input()))
    print('Введите стоимость доставок ед. товара')
    matrix, flag = cost(factory, shop)
    factory, shop = fictious(factory, shop, flag)
    reference_plan = n_w_angle(factory,shop)
    print('_' * 20)
    for k in range(len(reference_plan)):
        print(*reference_plan[k])
    print('Текущая цена', end = ': ')
    answer_this(reference_plan, matrix)
    print('_' * 20)
    f = open('output.txt','w', encoding = 'utf-8')
    while degeneracy(reference_plan, factory, shop):
        new_degeneracy(reference_plan)
    C_matrix = new_matrix(reference_plan, matrix)
    while min_elem(C_matrix) < 0:
        idx_x, idx_y = min_coord(C_matrix)
        reference_plan = next_plan(reference_plan, idx_x, idx_y)
        for i in range(len(reference_plan)):
            print(*reference_plan[i])
            foo =''
            for j in range(len(reference_plan[0])):
                foo += str(reference_plan[i][j]) + ' '
            f.write(foo + '\n')
        ans = answer_this(reference_plan, matrix)
        f.write('Текущая цена: ' + str(ans)+ '\n')
        print("_" * 20)
        f.write('_' * 20 + '\n')
        while degeneracy(reference_plan, factory, shop):
            new_degeneracy(reference_plan)
        C_matrix = new_matrix(reference_plan, matrix)
    for i in range(len(factory)):
        for j in range(len(shop)):
            if reference_plan[i][j] != 0:
                f.write(f"Направить из {i + 1} хранилища в {j + 1} заправочную станцию {reference_plan[i][j]} тонн горючего.\n")
    f.close()
process()