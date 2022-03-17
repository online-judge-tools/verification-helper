using System;
using System.Reflection;
// verification-helper: IGNORE
namespace Verifier
{
    public class LocalRunner
    {
        static void Main(string[] args)
        {
            string verifier;
            if (args.Length == 0)
            {
                Console.WriteLine("Input verifier name:");
                verifier = Console.ReadLine();
            }
            else
            {
                verifier = args[0];
            }
            var type = Type.GetType(verifier);

            var method = type.GetMethod("Main", BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
            method.Invoke(null, null);
        }
    }
}
