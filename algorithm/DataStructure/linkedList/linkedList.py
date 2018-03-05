# coding=utf-8
# uliontse


class LNode:
    def __init__(self,elem,next_=None):
        self.elem = elem
        self.next = next_


class LList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        n = 0
        p = self.head
        while p is not None:
            n += 1
            p = p.next
        return n

    def insertL(self,index,elem):
        if index <= 0:
            self.prepend(elem)
        if index >= self.length():
            self.append(elem)

        p = 0
        q = LNode(elem)
        for _ in range(index):
            p = self.head.next
        self.head.next = q
        q.next = p


    def prepend(self,elem):
        self.head = LNode(elem,self.head)

    def append(self,elem):
        if self.head is None:
            self.head = LNode(elem)
        else:
            p = self.head
            while p.next is not None:
                p = p.next
            p.next = LNode(elem)


    def pop(self):
        if self.head is None:
            raise Exception('PopError, now head is None!')
        e = self.head.elem
        self.head = self.head.next
        return e

    def pop_last(self):
        if self.head is None:
            raise Exception('Pop_lastError, now head is None!')
        p = self.head
        if p.next is None:
            e = p.elem
            self.head = None
            return e
        while p.next.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None
        return e

    def rev(self): #reverse
        p = None
        while self.head is not None:
            q = self.head
            self.head = q.next # 摘下原来首节点
            q.next = p
            p = q              # 将刚摘下的节点加入‘p引用的节点序列’
        self.head = p          # 反转后的节点序列已经完成，重置表头链接

    def print_all(self):
        p = self.head
        while p is not None:
            print(p.elem)
            p = p.next

    def elements(self): # 生成器
        p = self.head
        while p is not None:
            yield p.elem
            p = p.next

 
    def sort1(self): # 插入排序（倒换大元素）
        if self.head is None:
            return
        csr = self.head.next                    # csr: cursor
        while csr is not None:
            x = csr.elem
            p = self.head
            while p is not csr and p.elem <= x: # 跳过小元素
                p = p.next
            while p is not csr:                 # 倒换大元素，完成元素插入
                y = p.elem
                p.elem = x
                x = y
                p = p.next
            csr.elem = x
            csr = csr.next                      # 回填最后一个元素


    def sort2(self): # 插入排序（调整链接）
        p = self.head
        if p is None or p.next is None:
            return
        csr = p.next
        p.next = None
        while csr is not None:
            p = self.head
            q = None
            while p is not None and p.elem <= csr.elem:
                q = p
                p = p.next
            if q is None:
                self.head = csr
            else:
                q.next = csr
            q = csr
            csr = csr.next
            q.next = p

 

if __name__ == '__main__':
    llist = LList()
    # llist.pop()

    print('-' * 30)
    for i in range(3):
        llist.append(i)
    llist.rev()
    llist.print_all()

    print('-'*30)
    for _ in range(2):
        llist.insertL(1,100)
    llist.print_all()

    print('-'*30)
    llist.sort2()
    llist.print_all()
