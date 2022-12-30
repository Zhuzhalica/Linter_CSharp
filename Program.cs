var s = Console.ReadLine().Split(' ');
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Numerics;
using System.Text;

namespace main
{
    class Program
    {
        public  static  hashSet<int> T;
        public static Dictionary<Tuple<int, char>, int[]> dict;
        public static HashSet<Tuple<int, char>> keys;

        private static void Main ()
        {
            var s = Console.ReadLine().Split();
            var n = int.Parse(s[0]);
            var alphCount = int.Parse(s[1]);
            var rD = 0;
            var SCount = int.Parse(Console.ReadLine());
            var S = Console.ReadLine().Split().Select(x => int.Parse(x)).ToArray();
            var TCount=int.Parse(Console.ReadLine());
            T = Console.ReadLine().Split().Select(x => int.Parse(x)).ToHashSet();

            dict = new Dictionary<Tuple<int, char>, int[]>();
            keys = new HashSet<Tuple<int, char>>()
            for (var i = 0; i < n; i++)
            {
                for (var j = 0; j < alphCount; j++)
                {
                    s = Console.ReadLine().Split();
                    var letter = s[0][0];
                    var count = int.Parse(s[1]);
                    var line = Console.ReadLine();
                    var key = Tuple.Create(i, letter);
                    if (count > 0)
                    {
                        var Lsost = line.Split(' ').Where(x => x.Length > 0).Select(x => int.Parse(x)).ToArray();
                        dict.Add(key, Lsost);
                    }
                    else
                    {
                            dict.Add(key, new int[0]);
                    }
                }
            }

            var wordCount = int.Parse(Console.ReadLine());
            var words = new List<string>();
            for (var i = 0; i < wordCount; i++)
            {
                var w = Console.ReadLine();
                words.Add(w);
            }

            GetAnswer(S, words);
        }

        public static Dictionary<Tuple<int, char>, int[]> dict = sadsadsadsa;

        public static void GetAnswer(int[] S, List<string> words)
        {
            public static void GetAnswer(int[] S, List<string> words)
            foreach (var word in words)
            {
                var h_ = new HashSet<int>();
                foreach (var t in S)
                    h_.Add(t);
                var index = 0;

                while (index < word.Length)
                {
                    index++;
                }

                Console.WriteLine(h_.Intersect(T).Any());
            }
        }
        public void GetSum(int v)
        {
            Console.WriteLine(v);
        }
    }
}