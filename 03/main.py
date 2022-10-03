class CustomList(list):

    def __add__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        while len(l_list) != len(r_list):
            min(l_list, r_list, key=len).append(0)
        result = list(map(lambda x, y: x + y, l_list, r_list))
        return __class__(result)

    def __radd__(self, other):
        l_list = list(other).copy()
        r_list = list(self).copy()
        while len(l_list) != len(r_list):
            min(l_list, r_list, key=len).append(0)
        result = list(map(lambda x, y: x + y, l_list, r_list))
        return __class__(result)

    def __sub__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        while len(l_list) != len(r_list):
            min(l_list, r_list, key=len).append(0)
        result = list(map(lambda x, y: x - y, l_list, r_list))
        return __class__(result)

    def __rsub__(self, other):
        l_list = list(other).copy()
        r_list = list(self).copy()
        while len(l_list) != len(r_list):
            min(l_list, r_list, key=len).append(0)
        result = list(map(lambda x, y: x - y, l_list, r_list))
        return __class__(result)

    def __eq__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        return sum(l_list) == sum(r_list)

    def __ne__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        return sum(l_list) != sum(r_list)

    def __lt__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        return sum(l_list) < sum(r_list)

    def __le__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        return sum(l_list) <= sum(r_list)

    def __gt__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        return sum(l_list) > sum(r_list)

    def __ge__(self, other):
        l_list = list(self).copy()
        r_list = list(other).copy()
        return sum(l_list) >= sum(r_list)

    def __str__(self):
        m_list = list(self).copy()
        res = str(m_list)[1:-1] + ': ' + str(sum(m_list))
        return res
