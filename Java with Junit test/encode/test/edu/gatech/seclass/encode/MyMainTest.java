package edu.gatech.seclass.encode;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;
import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.Assert.*;

public class MyMainTest {
	
/*
Place all  of your tests in this class, optionally using MainTest.java as an example.
*/
    private ByteArrayOutputStream outStream;
    private ByteArrayOutputStream errStream;
    private PrintStream outOrig;
    private PrintStream errOrig;
    private Charset charset = StandardCharsets.UTF_8;

    @Rule
    public TemporaryFolder temporaryFolder = new TemporaryFolder();

    @Before
    public void setUp() throws Exception {
        outStream = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(outStream);
        errStream = new ByteArrayOutputStream();
        PrintStream err = new PrintStream(errStream);
        outOrig = System.out;
        errOrig = System.err;
        System.setOut(out);
        System.setErr(err);
    }

    @After
    public void tearDown() throws Exception {
        System.setOut(outOrig);
        System.setErr(errOrig);
    }

    // Some utilities

    private File createTmpFile() throws IOException {
        File tmpfile = temporaryFolder.newFile();
        tmpfile.deleteOnExit();
        return tmpfile;
    }

    private File createInputFile0() throws Exception {
        File file0 =  createTmpFile();
        FileWriter fileWriter = new FileWriter(file0);

        fileWriter.write("");

        fileWriter.close();
        return file0;
    }

    private File createInputFile1() throws Exception {
        File file1 =  createTmpFile();
        FileWriter fileWriter = new FileWriter(file1);

        fileWriter.write("abc $XYZ");

        fileWriter.close();
        return file1;
    }

    private File createInputFile2() throws Exception {
        File file2 =  createTmpFile();
        FileWriter fileWriter = new FileWriter(file2);

        fileWriter.write("hello");

        fileWriter.close();
        return file2;
    }

    private File createInputFile3() throws Exception {
        File file3 =  createTmpFile();
        FileWriter fileWriter = new FileWriter(file3);

        fileWriter.write("#hello$");

        fileWriter.close();
        return file3;
    }

    private File createInputFile4() throws Exception {
        File file4 =  createTmpFile();
        FileWriter fileWriter = new FileWriter(file4);

        fileWriter.write("HELLO");

        fileWriter.close();
        return file4;
    }

    private String getFileContent(String filename) {
        String content = null;
        try {
            content = new String(Files.readAllBytes(Paths.get(filename)), charset);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content;
    }


    // test cases

    // Purpose: <to test in case of the empty file>
    // Frame #: <test case 1 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest1() throws Exception {
        File inputFile0 = createInputFile0();

        String args[] = {inputFile0.getPath()};
        Main.main(args);

        String expected1 = "";

        String actual1 = getFileContent(inputFile0.getPath());

        assertEquals("The files differ!", expected1, actual1);
    }

    // Purpose: <to test in case of not empty file>
    // Purpose: <test with remove option but nothing specified to remove, method removes nothing from file>
    // Frame #: <test case 2 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest2() throws Exception {
        File inputFile1 = createInputFile1();

        String args[] = {"-d", "",inputFile1.getPath()};
        Main.main(args);

        String expected2 = "abc $XYZ";

        String actual2 = getFileContent(inputFile1.getPath());

        assertEquals("The files differ!", expected2, actual2);
    }

    // Purpose: <to test in case of not empty file>
    // Purpose: <test with remove option to remove all characters in file>
    // Frame #: <test case 3 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest3() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-d", "hello",inputFile2.getPath()};
        Main.main(args);

        String expected3 = "";

        String actual3 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected3, actual3);
    }

    // Purpose: <to test in case of not empty file and without space but with special character>
    // Purpose: <test without any option, performing default cipher function>
    // Frame #: <test case 18 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest4() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {inputFile3.getPath()};
        Main.main(args);

        String expected4 = "#olssv$";

        String actual4 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected4, actual4);
    }

    // Purpose: <to test in case of not empty file>
    // Purpose: <test with remove option to remove some uppercase letters in file>
    // Frame #: <test case 5 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest5() throws Exception {
        File inputFile1 = createInputFile1();

        String args[] = {"-d", "XYZ",inputFile1.getPath()};
        Main.main(args);

        String expected5 = "abc $";

        String actual5 = getFileContent(inputFile1.getPath());

        assertEquals("The files differ!", expected5, actual5);
    }

    // Purpose: <to test in case of not empty file>
    // Purpose: <test with remove option to remove some special character in file>
    // Frame #: <test case 6 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest6() throws Exception {
        File inputFile1 = createInputFile1();

        String args[] = {"-d", "$",inputFile1.getPath()};
        Main.main(args);

        String expected6 = "abc XYZ";

        String actual6 = getFileContent(inputFile1.getPath());

        assertEquals("The files differ!", expected6, actual6);
    }

    // Purpose: <to test in case of not empty file>
    // Purpose: <test with cipher option, but the input integer is zero, which means keep the letters as what they are>
    // Frame #: <test case 7 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest7() throws Exception {
        File inputFile1 = createInputFile1();

        String args[] = {"-c", "0",inputFile1.getPath()};
        Main.main(args);

        String expected7 = "abc $XYZ";

        String actual7 = getFileContent(inputFile1.getPath());

        assertEquals("The files differ!", expected7, actual7);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it without any option, method should encode the letter by the length of the file>
    // Frame #: <test case 10 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest8() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {inputFile2.getPath()};
        Main.main(args);

        String expected8 = "mjqqt";

        String actual8 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected8, actual8);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with cipher option to increment letters by a positive number>
    // Frame #: <test case 11 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest9() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-c", "5",inputFile2.getPath()};
        Main.main(args);

        String expected9 = "mjqqt";

        String actual9 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected9, actual9);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with reverse option only>
    // Frame #: <test case 12 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest10() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-r", inputFile2.getPath()};
        Main.main(args);

        String expected10 = "olleh";

        String actual10 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected10, actual10);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with reverse option & cipher option, incrementing by a positive integer>
    // Frame #: <test case 13 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest11() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-r", "-c", "5", inputFile2.getPath()};
        Main.main(args);

        String expected11 = "tqqjm";

        String actual11 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected11, actual11);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with remove option to remove some lowercase letters>
    // Frame #: <test case 14 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest12() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-d", "ll", inputFile2.getPath()};
        Main.main(args);

        String expected12 = "heo";

        String actual12 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected12, actual12);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with remove option to remove some lowercase letters & cipher option to increment letters by a positive integer>
    // Frame #: <test case 15 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest13() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-d", "el", "-c", "5", inputFile2.getPath()};
        Main.main(args);

        String expected13 = "mt";

        String actual13 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected13, actual13);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with remove option to remove some lowercase letters & reverse option>
    // Frame #: <test case 16 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest14() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-d", "el", "-r", inputFile2.getPath()};
        Main.main(args);

        String expected14 = "oh";

        String actual14 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected14, actual14);
    }

    // Purpose: <to test in case of not empty file without whitespace and only contains lowercase letters>
    // Purpose: <test it with all three options>
    // Frame #: <test case 17 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest15() throws Exception {
        File inputFile2 = createInputFile2();

        String args[] = {"-d", "el", "-r", "-c", "5", inputFile2.getPath()};
        Main.main(args);

        String expected15 = "tm";

        String actual15 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected15, actual15);
    }

    // Purpose: <to test in case of not empty file without whitespace but with special character>
    // Purpose: <test it with cipher function>
    // Frame #: <test case 19 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest16() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-c", "2",inputFile3.getPath()};
        Main.main(args);

        String expected16 = "#jgnnq$";

        String actual16 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected16, actual16);
    }

    // Purpose: <to test in case of not empty file without whitespace but with special character>
    // Purpose: <test it with reverse option only>
    // Frame #: <test case 20 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest17() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-r", inputFile3.getPath()};
        Main.main(args);

        String expected17 = "$olleh#";

        String actual17 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected17, actual17);
    }

    // Purpose: <to test in case of not empty file without whitespace but with special character>
    // Purpose: <test it with reverse option and cipher option>
    // Frame #: <test case 21 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest18() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-r", "-c", "25", inputFile3.getPath()};
        Main.main(args);

        String expected18 = "$nkkdg#";

        String actual18 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected18, actual18);
    }

    // Purpose: <to test in case of not empty file without whitespace and with special character>
    // Purpose: <test it with remove option only>
    // Frame #: <test case 22 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest19() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-d", "aeiou",inputFile3.getPath()};
        Main.main(args);

        String expected19 = "#hll$";

        String actual19 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected19, actual19);
    }

    // Purpose: <to test in case of not empty file without whitespace but with special character>
    // Purpose: <test it with remove option and cipher option>
    // Frame #: <test case 23 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest20() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-c", "2", "-d", "aeiou",inputFile3.getPath()};
        Main.main(args);

        String expected20 = "#jnn$";

        String actual20 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected20, actual20);
    }

    // Purpose: <to test in case of not empty file without whitespace but with special character>
    // Purpose: <test it with reverse option and remove function to remove one or more lowercase letters>
    // Frame #: <test case 24 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest21() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-r", "-d", "aeiou",inputFile3.getPath()};
        Main.main(args);

        String expected21 = "$llh#";

        String actual21 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected21, actual21);
    }

    // Purpose: <to test in case of not empty file without whitespace but with special character>
    // Purpose: <test it with all three options>
    // Frame #: <test case 25 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest22() throws Exception {
        File inputFile3 = createInputFile3();

        String args[] = {"-r", "-d", "aeiou","-c", "1", inputFile3.getPath()};
        Main.main(args);

        String expected22 = "$mmi#";

        String actual22 = getFileContent(inputFile3.getPath());

        assertEquals("The files differ!", expected22, actual22);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it without any option, perform default cipher function>
    // Frame #: <test case 26 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest23() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {inputFile4.getPath()};
        Main.main(args);

        String expected23 = "MJQQT";

        String actual23 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected23, actual23);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with cipher option>
    // Frame #: <test case 27 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest24() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-c", "2", inputFile4.getPath()};
        Main.main(args);

        String expected24 = "JGNNQ";

        String actual24 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected24, actual24);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with reverse option>
    // Frame #: <test case 28 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest25() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-r", inputFile4.getPath()};
        Main.main(args);

        String expected25 = "OLLEH";

        String actual25 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected25, actual25);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with reverse option and cipher option>
    // Frame #: <test case 29 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest26() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-r", "-c", "2", inputFile4.getPath()};
        Main.main(args);

        String expected26 = "QNNGJ";

        String actual26 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected26, actual26);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with remove function to remove lowercase some letters>
    // Frame #: <test case 30 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest27() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-d", "aeiou", inputFile4.getPath()};
        Main.main(args);

        String expected27 = "HLL";

        String actual27 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected27, actual27);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with remove function to remove lowercase some letters and cipher function>
    // Frame #: <test case 31 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest28() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-d", "aeiou", "-c", "2", inputFile4.getPath()};
        Main.main(args);

        String expected28 = "JNN";

        String actual28 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected28, actual28);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with remove function to remove lowercase some letters and reverse function>
    // Frame #: <test case 32 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest29() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-d", "aeiou", "-r",inputFile4.getPath()};
        Main.main(args);

        String expected29 = "LLH";

        String actual29 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected29, actual29);
    }

    // Purpose: <to test in case of not empty file without whitespace but with uppercase letters>
    // Purpose: <test it with all three functions>
    // Frame #: <test case 33 in the catpart.txt.tsl of A6>
    @Test
    public void encodeTest30() throws Exception {
        File inputFile4 = createInputFile4();

        String args[] = {"-d", "aeiou", "-r", "-c", "2", inputFile4.getPath()};
        Main.main(args);

        String expected30 = "NNJ";

        String actual30 = getFileContent(inputFile4.getPath());

        assertEquals("The files differ!", expected30, actual30);
    }
}
