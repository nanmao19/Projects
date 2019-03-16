package edu.gatech.seclass.encode;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {

    public static void main(String[] args)
    {
        if(args == null)
        {
            try
            {
                throw new NullPointerException();
            }
            catch (Exception e)
            {
                usage();
            }
        }

        else
        {
            String dString = "";
            int numShift = 0;
            boolean cipher = false, reverse = false, delete = false, fullReverse = false;
            String myFile = "";

            String filename = args[args.length - 1];

            //get original file content
            try
            {
                myFile = getFile(filename);
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
            System.out.print("Original File: ");
            System.out.println(myFile);


            for (int i = 0; i < args.length - 1; i++)
            {
                if (args[i].equals("-c"))
                {
                    cipher = true;
                    numShift = Integer.parseInt(args[i + 1]);
                    i++;
                }

                else if (args[i].equals("-r"))
                {
                    reverse = true;
                }

                else if (args[i].equals("-R"))
                {
                    fullReverse = true;
                }

                else if (args[i].equals("-d"))
                {
                    delete = true;
                    dString = args[i + 1];
                    i++;
                }

                else
                {
                    usage();
                }
            }

            if (delete) //remove characters function
            {
                if (dString.equals(" ")) //removed space
                {
                    myFile = myFile.replaceAll("\\s","");
                }
                else if (dString.equals("\r"))
                {
                    myFile = myFile.replaceAll("\\r","");
                }

                myFile = removeChar(myFile, dString);

                BufferedWriter writer = null;
                try
                {
                    writer = new BufferedWriter(new FileWriter(filename));
                    writer.write(myFile);
                    writer.close();
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }

                System.out.print("Characters Removed File: ");
                System.out.println(myFile);
            }

            if (cipher) //cipher function
            {
                myFile = cipher(myFile, numShift);

                try
                {
                    BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
                    writer.write(myFile);
                    writer.close();}
                catch(IOException e)
                {
                    e.printStackTrace();
                }

                System.out.print("Encoded File: ");
                System.out.println(myFile);
            }

            if (reverse) //reverse function
            {
                try
                {
                    myFile = reverseFile(myFile);

                    try
                    {
                        BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
                        writer.write(myFile);
                        writer.close();
                    }
                    catch(IOException e)
                    {
                        e.printStackTrace();
                    }

                    System.out.print("Reversed File: ");
                    System.out.println(myFile);
                }
                catch (StringIndexOutOfBoundsException e)
                {
                    System.err.println("File Not Found");
                }
            }

            if (fullReverse)
            {
                 myFile = reverseWords(myFile);

                 try
                 {
                    BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
                    writer.write(myFile);
                    writer.close();
                 }
                 catch(IOException e)
                 {
                     e.printStackTrace();
                 }

                 System.out.print("Fully Reversed File: ");
                 System.out.println(myFile);
            }

            if (!delete && !cipher && !reverse && !fullReverse) //default function
            {
                numShift = myFile.length();
                myFile = cipher(myFile, numShift);

                try
                {
                    BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
                    writer.write(myFile);
                    writer.close();
                }
                catch(IOException e)
                {
                    e.printStackTrace();
                }

                System.out.print("Default Encoded File: ");
                System.out.println(myFile);

            }
        }
    }

    //print charArray
    public static void printCharArray(char[] arr) {
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i]);
        }
        System.out.println();
    }


    //convert string array to char array
    public static char[] convertToCharArray(String[] sArray) {
        String s = "";
        for (String n : sArray)
            s += n;
        char[] ch = s.toCharArray();
        return ch;
    }

    //get file content by file name to charArray
    public static String getFile(String filename) throws IOException
    {
        String content = null;

        Charset charset = StandardCharsets.UTF_8;
        try
        {
            content = new String(Files.readAllBytes(Paths.get(filename)), charset);
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return content;
    }

    //remove character in file function
    public static String removeChar(String file, String d)
    {
        String[] removedS = d.split("\\s");

        char[] removedC = convertToCharArray(removedS);

        System.out.print("remove characters: ");
        printCharArray(removedC);

        for (int i = 0; i < removedC.length; i++)
        {

            int ascii = (int)removedC[i];

            if (ascii >= 65 && ascii <= 90) //removed input in uppercase letter
            {
                String temp1 = String.valueOf((char)ascii);

                file = file.replaceAll(temp1,""); //remove this uppercase letter

                int asciiLower = ascii + 32; //convert to corresponding lowercase letter

                temp1 = String.valueOf((char)asciiLower);

                file = file.replaceAll(temp1,""); //remove corresponding lowercase letter
            }

            else if (ascii >= 97 && ascii <= 122) //removed input in lowercase letter
            {
                String temp2 = String.valueOf((char)ascii);

                file = file.replaceAll(temp2,""); //remove this lowercase letter

                int asciiUpper = ascii - 32; //convert to corresponding uppercase letter

                temp2 = String.valueOf((char)asciiUpper);

                file = file.replaceAll(temp2,""); //remove corresponding uppercase letter
            }

            else if (removedC[i]=='*')//removed *
            {
                file = file.replaceAll("\\*","");
            }

            else if (removedC[i]=='$')//removed $
            {
                file = file.replaceAll("[$,]","");
            }


            else //removed number or special characters
            {
                String temp3 = String.valueOf((char)ascii);

                file = file.replaceAll(temp3,""); }

        }

        return file;
    }

    //encode file function
    public static String cipher(String file, int shift) throws java.util.regex.PatternSyntaxException
    {
        String[] sArray = file.split("");

        char[] fileArray = convertToCharArray(sArray);

        for (int j = 0; j < fileArray.length; j++)
        {
            int ascii = (int) fileArray[j];

            if (ascii >= 65 && ascii <= 90) //shift within uppercase letters
            {
                int shift1 = shift % 26;

                int shifted1 = ascii + shift1;

                if (shifted1 > 90 ) //wrap back to A or a
                {
                    shifted1 = ascii + shift1 - 26;
                }

                else if (shifted1 < 65) //wrap back to Z or z
                {
                    shifted1 = ascii + shift1 + 26;
                }

                fileArray[j] = (char) shifted1;
            }

            else if (ascii >= 97 && ascii <= 122)//shift within lowercase letters
            {
                int shift2 = shift % 26;

                int shifted2 = ascii + shift2;

                if (shifted2 > 122 ) //wrap back to A or a
                {
                    shifted2 = ascii + shift2 - 26;
                }

                else if (shifted2 < 97) //wrap back to Z or z
                {
                    shifted2 = ascii + shift2 + 26;
                }

                fileArray[j] = (char) shifted2;
            }

            else if (ascii >= 48 && ascii <= 57)//shift within numbers
            {
                int shift3 = shift % 10;

                int shifted3 = ascii + shift3;

                if (shifted3 > 57) //wrap back to 0
                {
                    shifted3 = ascii + shift3 - 10;
                }

                else if (shifted3 < 48) //wrap back to 9
                {
                    shifted3 = ascii + shift3 + 10;
                }

                fileArray[j] = (char) shifted3;
            }
        }

        file = new String(fileArray);
        return file;
    }

    //reverse each word function
    public static String reverseFile(String file) {

        //split string file by lines
        file = file.replaceAll("\r","\r\n");
        String[] lines = file.split("\\n");

        file = "";

        for (String line : lines)
        {
            char end = line.charAt(line.length()-1);

            if (end == '\r' && !Character.isWhitespace(line.charAt(line.length()-2)))
            {
                line = reverseLine (line);

                file = file + line + "\r";
            }

            else if (end == '\r' && Character.isWhitespace(line.charAt(line.length()-2)))
            {
                line = reverseLine (line);

                file = file + line + " " + "\r";
            }

            else if (Character.isWhitespace(line.charAt(line.length()-1)))
            {
                line = reverseLine (line);

                file = file + line + " " + System.getProperty("line.separator");
            }
            else
            {
                line = reverseLine (line);

                file = file + line + System.getProperty("line.separator");
            }
        }

        file = file.trim();

        return file;
    }

    public static String reverseLine (String str)
    {
        String[] sArray = str.split("\\s");

        for (int i = 0; i < sArray.length; i++)
        {
            sArray[i] = new StringBuilder(sArray[i]).reverse().toString();
        }

        str = String.join(" ", sArray);

        return str;
    }

    //Full reverse function
    public static String reverseWords(String file)
    {
        //split string file by lines
        file = file.replaceAll("\r","\r\n");

        String[] lines = file.split("\n");

        file = "";

        for (String line : lines)
        {
            String temp = "";

            char end = line.charAt(line.length()-1);

            if (end == '\r' && !Character.isWhitespace(line.charAt(line.length()-2)))
            {
                temp = "";
            }
            else if (Character.isWhitespace(line.charAt(line.length()-1)))
            {
                temp = " ";
            }

            String[] sArray = line.split("\\s");

            for (int i = sArray.length-1; i >= 0; i--)
            {
                if (i==0)
                {
                    temp = temp + sArray[i];
                }
                else
                {
                    temp = temp + sArray[i] + " ";
                }
            }

            line = temp;

            if(end == '\r')
            {
                file =  "\r" + line + file;
            }
            else
            {
                file =  System.getProperty("line.separator") + line + file;
            }
        }

        file  = file.trim();

        return file;
    }

    private static void usage() {
        System.err.println("Usage: Encode  [-c int] [-d string] [-r] [-R] <filename>");
    }
}