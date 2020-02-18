class SegmentTree<T>
{
    public int Count { get; private set; }
    T Identity;
    T[] Data;
    Func<T, T, T> Merge;
    int LeafCount;
    public SegmentTree(int count, T identity, Func<T, T, T> merge)
    {
        Count = count;
        Identity = identity;
        Merge = merge;
        LeafCount = 1;
        while (LeafCount < count) LeafCount <<= 1;
        Data = new T[LeafCount << 1];
        for (int i = 1; i < Data.Length; i++) Data[i] = identity;
    }
    public T this[int index]
    {
        get { return Data[LeafCount + index]; }
        set { Assign(index, value); }
    }
    public void Assign(int i, T x) { Data[i += LeafCount] = x; while (0 < (i >>= 1)) Data[i] = Merge(Data[i << 1], Data[(i << 1) | 1]); }
    public void Operate(int i, T x) { Data[i += LeafCount] = Merge(Data[i], x); while (0 < (i >>= 1)) Data[i] = Merge(Data[i << 1], Data[(i << 1) | 1]); }
    public T Slice(int l, int length) => Fold(l, l + length);
    public T Fold(int l, int r)
    {
        T lRes = Identity, rRes = Identity;
        for (l += LeafCount, r += LeafCount - 1; l <= r; l = (l + 1) >> 1, r = (r - 1) >> 1)
        {
            if ((l & 1) == 1) lRes = Merge(lRes, Data[l]);
            if ((r & 1) == 0) rRes = Merge(Data[r], rRes);
        }
        return Merge(lRes, rRes);
    }
}
