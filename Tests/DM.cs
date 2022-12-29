using System;
using System.Collections.Generic;
using System.Linq;

namespace ConsoleApp2
{
    public static class Program
    {
        public static void Main(string[] args)
        {
            var _ = int.Parse(Console.ReadLine()!);
            var literalClauses = new Dictionary<int, HashSet<int>>();
            var clauses = new Dictionary<int, HashSet<int>>();
            var implicationsRight = new Dictionary<int, int>();
            var requiredLiterals = new HashSet<int>();
            var isFailed = false;

            var firstViewCount = int.Parse(Console.ReadLine()!);
            var setFirst = new HashSet<int>();
            for (var i = 0; i < firstViewCount; i++)
            {
                var c = int.Parse(Console.ReadLine()!);
                setFirst.Add(c);
            }

            var secondView = int.Parse(Console.ReadLine()!);
            for (var i = 0; i < secondView; i++)
            {
                clauses[i] = new HashSet<int>();
                var d = Console.ReadLine()!.Split();
                var dA = d.Skip(1).Take(d.Length - 2).Select(int.Parse).ToList();
                implicationsRight[i] = int.Parse(d.Last());

                foreach (var literal in dA)
                {
                    if (!literalClauses.ContainsKey(literal))
                    {
                        literalClauses[literal] = new HashSet<int>();
                    }

                    if (!setFirst.Contains(literal))
                    {
                        clauses[i].Add(literal);
                        literalClauses[literal].Add(i);
                    }
                }

                if (clauses[i].Count == 0 && !setFirst.Contains(implicationsRight[i]))
                {
                    requiredLiterals.Add(implicationsRight[i]);
                }
            }

            var thirdView = int.Parse(Console.ReadLine()!);
            for (var i = secondView; i < secondView + thirdView; i++)
            {
                clauses[i] = new HashSet<int>();
                var e = Console.ReadLine()!.Split();
                var eB = e.Skip(1).Select(int.Parse).ToList();

                foreach (var literal in eB)
                {
                    if (!literalClauses.ContainsKey(literal))
                    {
                        literalClauses[literal] = new HashSet<int>();
                    }

                    if (!setFirst.Contains(literal))
                    {
                        clauses[i].Add(literal);
                        literalClauses[literal].Add(i);
                    }
                }

                if (clauses[i].Count == 0)
                {
                    isFailed = true;
                    break;
                }
            }

            var listFirst = setFirst.ToList();
            listFirst.AddRange(requiredLiterals);
            setFirst = listFirst.ToHashSet();


            while (requiredLiterals.Count != 0 && !isFailed)
            {
                var currentLiteral = requiredLiterals.Last();
                requiredLiterals.Remove(currentLiteral);
                if (literalClauses.ContainsKey(currentLiteral))
                {
                    foreach (var clauseIndex in literalClauses[currentLiteral])
                    {
                        clauses[clauseIndex].Remove(currentLiteral);
                        if (clauses[clauseIndex].Count == 0)
                        {
                            if (implicationsRight.ContainsKey(clauseIndex))
                            {
                                if (setFirst.Contains(implicationsRight[clauseIndex])) continue;
                                requiredLiterals.Add(implicationsRight[clauseIndex]);
                                setFirst.Add(implicationsRight[clauseIndex]);
                            }
                            else
                            {
                                isFailed = true;
                                break;
                            }
                        }
                    }
                }
            }

            if (isFailed)
            {
                Console.WriteLine(-1);
            }
            else
            {
                Console.WriteLine(setFirst.Count);
                foreach (var ans in setFirst)
                {
                    Console.Write(ans + " ");
                }
            }
        }
    }
}