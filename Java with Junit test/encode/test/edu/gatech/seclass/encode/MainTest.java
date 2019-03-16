package edu.gatech.seclass.encode;

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

/*
DO NOT ALTER THIS CLASS.  Use it as an example for MyMainTest.java
 */

public class MainTest {

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

    /*
    *  TEST UTILITIES
    */

    // Create File Utility
    private File createTmpFile() throws Exception {
        File tmpfile = temporaryFolder.newFile();
        tmpfile.deleteOnExit();
        return tmpfile;
    }

    // Write File Utility
    private File createInputFile(String input) throws Exception {
        File file =  createTmpFile();

        OutputStreamWriter fileWriter =
                     new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8);

        fileWriter.write(input);

        fileWriter.close();
        return file;
    }


    //Read File Utility
    private String getFileContent(String filename) {
        String content = null;
        try {
            content = new String(Files.readAllBytes(Paths.get(filename)), charset);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content;
    }



    /*
    *  TEST FILES - refactored for readability w/ repeated file creation methods
    */

    private static final String FILE1 = "abcxyz";
    private static final String FILE2 = "Howdy Billy,\n" +
            "I am going to take cs6300 and cs6400 next semester.\n" +
            "Did you take cs 6300 last semester? I want to\n" +
            "take 2 courses so that I will graduate Asap!";
    private static final String FILE3 = "abc123";
    private static final String FILE4 = "";
    private static final String FILE5 = " ";
    private static final String FILE6 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private static final String FILE7 = "0123456789";
    private static final String FILE8 = "Let's try some **special**  %!(characters)!% ###\n" +
                                        "and line breaks^$@ \r" +
                                        "of \\different// types; \n" +
                                        "in 1 file\r"+
                                        ":-)";
    private static final String FILE9 = "Up with the white and gold\r" +
            "Down with the red and black\r" +
            "Georgia Tech is out for a victory\r" +
            "Well drop a battle axe on georgia's head\r" +
            "When we meet her our team is sure to beat her\r" +
            "Down on the old farm there will be no sound\r" +
            "'Till our bow wows rips through the air\r" +
            "When the battle is over georgia's team will be found\r" +
            "With the Yellow Jacket's swarming 'round! Hey!";
    private static final String FILE10 = "Robert'); DROP TABLE students;--";
    private static final String FILE11 = ".*";
    private static final String FILE12 = " Just a one line file with numbers 123456 ";
    private static final String FILE13 = "Howdy Billy," + System.lineSeparator() +
            "I am going to take cs6300 and cs6400 next semester."  + System.lineSeparator() +
            "Did you take cs 6300 last semester? I want to"  + System.lineSeparator() +
            "take 2 courses so that I will graduate Asap!";
    private static final String FILE14 = "\n";


    /*
    *   TEST CASES
    */

    // Purpose: To provide an example of a test case format
    // Frame #: Instructor example 1 from assignment directions
    @Test
    public void mainTest1() throws Exception {
        File inputFile1 = createInputFile(FILE1);

        String args[] = {inputFile1.getPath()};
        Main.main(args);

        String expected1 = "ghidef";

        String actual1 = getFileContent(inputFile1.getPath());

        assertEquals("The files differ!", expected1, actual1);
    }

    // Purpose: To provide an example of a test case format
    // Frame #: Instructor example 2 from assignment directions
    @Test
    public void mainTest2() throws Exception {
        File inputFile2 = createInputFile(FILE2);

        String args[] = {"-r", inputFile2.getPath()};
        Main.main(args);

        String expected2 = "ydwoH ,ylliB\n" +
                "I ma gniog ot ekat 0036sc dna 0046sc txen .retsemes\n" +
                "diD uoy ekat sc 0036 tsal ?retsemes I tnaw ot\n" +
                "ekat 2 sesruoc os taht I lliw etaudarg !pasA";

        String actual2 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected2, actual2);
    }

    // Purpose: To provide an example of a test case format
    // Frame #: Instructor example 3 from assignment directions
    @Test
    public void mainTest3() throws Exception {
        File inputFile2 = createInputFile(FILE2);

        String args[] = {"-d", "aeiou", "-c", "3", inputFile2.getPath()};
        Main.main(args);

        String expected3 = "Kzgb Eoob,\n"
                + " p jqj w wn fv9633 qg fv9733 qaw vpvwu.\n"
                + "Gg b wn fv 9633 ovw vpvwu?  zqw w\n"
                + "wn 5 fuvv v wkw  zoo jugw vs!";

        String actual3 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected3, actual3);
    }

    // Purpose: To provide an example of a test case format
    // Frame #: Instructor example 4 from assignment directions
    @Test
    public void mainTest4() throws Exception {
        File inputFile2 = createInputFile(FILE2);

        String args[] = {"-c", "2", inputFile2.getPath()};
        Main.main(args);

        String expected4 = "Jqyfa Dknna,\n"
                + "K co iqkpi vq vcmg eu8522 cpf eu8622 pgzv ugoguvgt.\n"
                + "Fkf aqw vcmg eu 8522 ncuv ugoguvgt? K ycpv vq\n"
                + "vcmg 4 eqwtugu uq vjcv K yknn itcfwcvg Cucr!";

        String actual4 = getFileContent(inputFile2.getPath());

        assertEquals("The files differ!", expected4, actual4);
    }


    // Purpose: To provide an example of a test case format
    // Frame #: Instructor error example
    @Test
    public void mainTest5() {
        String args[] = null; //invalid argument
        Main.main(args);
        assertEquals("Usage: Encode  [-c int] [-d string] [-r] [-R] <filename>", errStream.toString().trim());
    }

    // Purpose: To provide an example of a test case format
    // Frame #: Instructor example 1 from updated assignment directions
    @Test
    public void mainTest6() throws Exception {
        File inputFile = createInputFile(FILE3);

        String args[] = {inputFile.getPath()};
        Main.main(args);

        String expected = "ghi789";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest7() throws Exception {
        File inputFile = createInputFile(FILE4);

        String args[] = {"-c", "2", inputFile.getPath()};
        Main.main(args);

        String expected = "";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest8() throws Exception {
        File inputFile = createInputFile(FILE8);

        String args[] = {"-r", inputFile.getPath()};
        Main.main(args);

        String expected = "s'teL yrt emos **laiceps**  %!)sretcarahc(!% ###\n" +
                "dna enil @$^skaerb \r" +
                "fo //tnereffid\\ ;sepyt \n" +
                "ni 1 elif\r" +
                ")-:";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest9() throws Exception {
        File inputFile = createInputFile(FILE8);

        String args[] = {"-R", inputFile.getPath()};
        Main.main(args);

        String expected = ":-)\r" +
                "file 1 in\n" +
                " types; \\different// of\r" +
                " breaks^$@ line and\n" +
                "### %!(characters)!%  **special** some try Let's";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest10() throws Exception {
        File inputFile = createInputFile(FILE13);

        String args[] = {"-c", "-5", inputFile.getPath()};
        Main.main(args);

        String expected = "Cjryt Wdggt," + System.lineSeparator() +
                "D vh bjdib oj ovfz xn1855 viy xn1955 izso nzhznozm." + System.lineSeparator() +
                "Ydy tjp ovfz xn 1855 gvno nzhznozm? D rvio oj" + System.lineSeparator() +
                "ovfz 7 xjpmnzn nj ocvo D rdgg bmvypvoz Vnvk!";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest11() throws Exception {
        File inputFile = createInputFile(FILE5);

        String args[] = {inputFile.getPath()};
        Main.main(args);

        String expected = " ";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest12() throws Exception {
        File inputFile = createInputFile(FILE6);

        String args[] = {"-c", "-5", inputFile.getPath()};
        Main.main(args);

        String expected = "vwxyzabcdefghijklmnopqrstuVWXYZABCDEFGHIJKLMNOPQRSTU";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest13() throws Exception {
        File inputFile = createInputFile(FILE6);

        String args[] = {"-c", "58", "-R", inputFile.getPath()};
        Main.main(args);

        String expected = "ghijklmnopqrstuvwxyzabcdefGHIJKLMNOPQRSTUVWXYZABCDEF";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest14() throws Exception {
        File inputFile = createInputFile(FILE7);

        String args[] = {"-c", "-1", inputFile.getPath()};
        Main.main(args);

        String expected = "9012345678";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest15() throws Exception {
        File inputFile = createInputFile(FILE7);

        String args[] = {"-c", "10", "-r", inputFile.getPath()};
        Main.main(args);

        String expected = "9876543210";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest16() throws Exception {
        File inputFile = createInputFile(FILE13);

        String args[] = {"-c", "78", inputFile.getPath()};
        Main.main(args);

        String expected = "Howdy Billy," + System.lineSeparator() +
                "I am going to take cs4188 and cs4288 next semester."  + System.lineSeparator() +
                "Did you take cs 4188 last semester? I want to"  + System.lineSeparator() +
                "take 0 courses so that I will graduate Asap!";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest17() throws Exception {
        File inputFile = createInputFile(FILE8);

        String args[] = {"-c", "-76", inputFile.getPath()};
        Main.main(args);

        String expected = "Ngv'u vta uqog **urgekcn**  %!(ejctcevgtu)!% ###\n" +
                "cpf nkpg dtgcmu^$@ \r" +
                "qh \\fkhhgtgpv// vargu; \n" +
                "kp 5 hkng\r" +
                ":-)";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest18() throws Exception {
        File inputFile = createInputFile(FILE8);

        String args[] = {"-d", "*", inputFile.getPath()};
        Main.main(args);

        String expected = "Let's try some special  %!(characters)!% ###\n" +
                "and line breaks^$@ \r" +
                "of \\different// types; \n" +
                "in 1 file\r" +
                ":-)";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest19() throws Exception {
        File inputFile = createInputFile(FILE12);

        String args[] = {"-R", "-r", "-d", " ", inputFile.getPath()};
        Main.main(args);

        String expected = "654321srebmunhtiwelifenilenoatsuJ";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest20() throws Exception {
        File inputFile = createInputFile(FILE10);

        String args[] = {"-d", "-r", inputFile.getPath()};
        Main.main(args);

        String expected = "obet'); DOP TABLE students;";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest21() throws Exception {
        File inputFile = createInputFile(FILE11);

        String args[] = {"-d", "a", inputFile.getPath()};
        Main.main(args);

        String expected = ".*";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest22() throws Exception {
        File inputFile = createInputFile(FILE11);

        String args[] = {"-r", inputFile.getPath()};
        Main.main(args);

        String expected = "*.";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest23() throws Exception {
        File inputFile = createInputFile(FILE12);

        String args[] = {"-r-c", inputFile.getPath()};
        Main.main(args);

        assertEquals("Usage: Encode  [-c int] [-d string] [-r] [-R] <filename>", errStream.toString().trim());
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest24() throws Exception {
        File inputFile = createInputFile(FILE1);

        String args[] = {"-d", "zyxcab", inputFile.getPath()};
        Main.main(args);

        String expected = "";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest25() throws Exception {

        String args[] = {"-r", "filedoesnotexist.txt"};
        Main.main(args);

        assertEquals("File Not Found", errStream.toString().trim());
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest26() throws Exception {
        File inputFile = createInputFile(FILE9);

        String args[] = {"-r", "-d", "\r", "-c", "5", "-R", inputFile.getPath()};
        Main.main(args);

        String expected = "!djM !isztw' lsnrwfbx x'yjphfO btqqjD jmy mynBisztk jg qqnb rfjy x'fnlwtjl wjat xn " +
                "jqyyfg jmy sjmBwnf jmy mlztwmy xunw xbtb btg wzt qqnY'isztx ts jg qqnb jwjmy rwfk iqt jmy st " +
                "sbtIwjm yfjg ty jwzx xn rfjy wzt wjm yjjr jb sjmBifjm x'fnlwtjl st jcf jqyyfg f utwi qqjBdwtyhna " +
                "f wtk yzt xn mhjY fnlwtjLphfqg isf ijw jmy mynb sbtIiqtl isf jynmb jmy mynb uZ";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest27() throws Exception {
        File inputFile = createInputFile(FILE9);

        String args[] = {"-c", "10", "-c", "3", inputFile.getPath()};
        Main.main(args);

        String expected = "Xs zlwk wkh zklwh dqg jrog\r" +
                "Grzq zlwk wkh uhg dqg eodfn\r" +
                "Jhrujld Whfk lv rxw iru d ylfwrub\r" +
                "Zhoo gurs d edwwoh dah rq jhrujld'v khdg\r" +
                "Zkhq zh phhw khu rxu whdp lv vxuh wr ehdw khu\r" +
                "Grzq rq wkh rog idup wkhuh zloo eh qr vrxqg\r" +
                "'Wloo rxu erz zrzv ulsv wkurxjk wkh dlu\r" +
                "Zkhq wkh edwwoh lv ryhu jhrujld'v whdp zloo eh irxqg\r" +
                "Zlwk wkh Bhoorz Mdfnhw'v vzduplqj 'urxqg! Khb!";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest28() throws Exception {
        File inputFile = createInputFile(FILE14);

        String args[] = {"-c", "-30", inputFile.getPath()};
        Main.main(args);

        String expected = "\n";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest29() throws Exception {
        File inputFile = createInputFile(FILE9);

        String args[] = {"-R", "-r", inputFile.getPath()};
        Main.main(args);

        String expected = "!yeH !dnuor' gnimraws s'tekcaJ wolleY eht htiW\r" +
                "dnuof eb lliw maet s'aigroeg revo si elttab eht nehW\r" +
                "ria eht hguorht spir swow wob ruo lliT'\r" +
                "dnuos on eb lliw ereht mraf dlo eht no nwoD\r" +
                "reh taeb ot erus si maet ruo reh teem ew nehW\r" +
                "daeh s'aigroeg no exa elttab a pord lleW\r" +
                "yrotciv a rof tuo si hceT aigroeG\r" +
                "kcalb dna der eht htiw nwoD\r" +
                "dlog dna etihw eht htiw pU";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

    // Purpose: New Test Case for Refactoring
    // Frame #: Instructor Provided New Test Case
    @Test
    public void mainTest30() throws Exception {
        File inputFile = createInputFile(FILE10);

        String args[] = {"-r", inputFile.getPath()};
        Main.main(args);

        String expected = ";)'treboR PORD ELBAT --;stneduts";

        String actual = getFileContent(inputFile.getPath());

        assertEquals("The files differ!", expected, actual);
    }

}
