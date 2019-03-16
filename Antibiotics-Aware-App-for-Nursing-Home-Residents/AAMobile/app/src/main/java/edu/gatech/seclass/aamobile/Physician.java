package edu.gatech.seclass.aamobile;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.RadioButton;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class Physician extends AppCompatActivity {

    private String TAG = Physician.class.getSimpleName();
    ArrayList<HashMap<String, String>> patientList;
    private ListView lv;
    private String selectedItem, selectedID;


    private JSONArray dataArray = new JSONArray();
    private JSONObject data = new JSONObject();
    private JSONObject patient = new JSONObject();
    private JSONObject background = new JSONObject();
    private JSONObject assessment = new JSONObject();
    private JSONObject vitals = new JSONObject();
    private JSONObject withIndwellingCatheter = new JSONObject();
    private JSONObject withoutIndwellingCatheter = new JSONObject();
    private JSONObject labs = new JSONObject();

    //Patient info strings from JSON
    private String indivID, indivPatientName, indivDate, indivAge, indivGender;
    //Background info strings from JSON
    private String indivCatheter, indivIncontinence, indivUTI6, indivPyelonephritis, indivProstatitis, indivPenicillinAllergy;
    //Nurse Notes info strings from JSON
    private String indivNurseNoteOrganisms, indivNurseNoteTreatment, indivNurseNoteDiagnosis, indivNurseNoteDirectives;
    //Vitals info strings from JSON
    private String indivWeight, indivBpLow, indivBpHigh, indivHr, indivRespRate, indivTemp, indivO2;
    //Catheter Assessment Page
    private String withORwithoutCath;
    private String assess1, assess2, assess3, assess4, assess5, assess6, assess7, assess8, assess9;
    //Labs serumCreatinine string value from JSON
    private String indivSerumCreatinine;

    // Next workflow buttons
    private Button buttonAcknowledge, buttonNext, buttonSubmit;

    //Common Buttons
    private Button buttonLogout, buttonBack;
    private Button buttonHome;

    private String selectDrug;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.physician1_sbar_notifications);
        buttonLogout = findViewById(R.id.logout_button);

        patientList = new ArrayList<>();
        lv = findViewById(R.id.list);

        new GetSBARs().execute();
        clickSBAR();

        // click Logout button
        buttonLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(i);
            }
        });

    }

    @Override
    public void onBackPressed() {
        Intent i = new Intent(this, Physician.class);
        startActivity(i);
    }

    public void PhysicianSBARreview() {

        new GetIndividualSBAR().execute();

        setContentView(R.layout.physician2_review_sbar);
        buttonBack = findViewById(R.id.back_review);
        buttonAcknowledge = findViewById(R.id.acknowledgement);

        buttonAcknowledge.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                PhysicianRecommendation();

            }
        });

        //Back button to restart physician workflow
        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });


    }

    // Same JSON get code from the JSON Util Nurse activity
    public class GetSBARs extends AsyncTask<Void, Void, Void> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Toast.makeText(Physician.this, "Loading Submitted SBARs", Toast.LENGTH_SHORT).show();
        }

        @Override
        protected Void doInBackground(Void... arg0) {
            HttpHandler sh = new HttpHandler();
            // Making a request to url and getting response
            //String url = "http://localhost:5000/api/patients";
            String url = "https://cs6440-f18-prj34.apps.hdap.gatech.edu/api/patients";

            String jsonStr = sh.makeServiceCall(url);

            Log.e(TAG, "Response from url: " + jsonStr);
            if (jsonStr != null) {
                try {
                    //System.out.println(jsonStr);
                    JSONObject jsonObj = new JSONObject(jsonStr);

                    // Getting JSON Array node
                    dataArray = jsonObj.getJSONArray("data");

                    // looping through All Contacts
                    for (int i = 0; i < dataArray.length(); i++) {
                        String uticoncern;
                        JSONObject c = dataArray.getJSONObject(i);
                        // Patient node is JSON object within the data array.
                        patient = c.getJSONObject("patientinfo");
                        String id = patient.getString("id");
                        if (patient.has("uticoncern")) {
                            uticoncern = "UTI Concern: " + patient.getString("uticoncern");
                        } else {
                            uticoncern = "N/A";
                        }

                        // Background node is JSON Object within the data array.
                        background = c.getJSONObject("background");

                        // tmp hash map for single patient
                        HashMap<String, String> patients = new HashMap<>();

                        // adding each child node to HashMap key => value
                        patients.put("id", id);
                        patients.put("uticoncern", uticoncern);

                        // adding contact to contact list
                        patientList.add(patients);
                    }
                } catch (final JSONException e) {
                    Log.e(TAG, "Json parsing error: " + e.getMessage());
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(),
                                    "Json parsing error: " + e.getMessage(),
                                    Toast.LENGTH_LONG).show();
                        }
                    });

                }

            } else {
                Log.e(TAG, "Couldn't get json from server.");
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(),
                                "Couldn't get json from server. Check LogCat for possible errors!",
                                Toast.LENGTH_LONG).show();
                    }
                });
            }

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);
            ListAdapter adapter = new SimpleAdapter(Physician.this, patientList,
                    R.layout.list_item, new String[]{"id", "uticoncern"},
                    new int[]{R.id.id, R.id.uticoncern});
            lv.setAdapter(adapter);
        }
    }

    public void clickSBAR() {

        // Set an item click listener for ListView
        lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                // Get the selected item text from ListView
                Log.e(TAG, "Selected Item: " + parent.getItemAtPosition(position));
                selectedItem = String.valueOf(parent.getItemAtPosition(position));

                //extracting ID numbers
                selectedID = selectedItem.replaceAll("[^0-9]", "");
                System.out.println("ID is: " + selectedID);

                Toast.makeText(Physician.this, "SBAR Selected: " + selectedItem, Toast.LENGTH_SHORT).show();

                PhysicianSBARreview();
            }
        });
    }

    public class GetIndividualSBAR extends AsyncTask<Void, Void, Void> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Toast.makeText(Physician.this, "Loading Patient SBAR", Toast.LENGTH_SHORT).show();
        }

        @Override
        protected Void doInBackground(Void... arg0) {
            HttpHandler sh = new HttpHandler();
            // Making a request to url and getting response

            //String url = "http://localhost:5000/api/patients";
            String url = "https://cs6440-f18-prj34.apps.hdap.gatech.edu/api/patients/" + selectedID;
            String jsonStr = sh.makeServiceCall(url);

            Log.e(TAG, "Response from url - Full JSON: " + jsonStr);
            if (jsonStr != null) {
                try {
                    //System.out.println(jsonStr);
                    JSONObject jsonObj = new JSONObject(jsonStr);
                    // Getting JSON Array node
                    data = jsonObj.getJSONObject("data");

                    Log.e(TAG, "Response from url - Array: " + data);

                    // Patient node is JSON object within the data array.
                    patient = data.getJSONObject("patientinfo");
                    indivID = patient.getString("id");
                    indivDate = patient.getString("date");
                    //indivAge = patient.getString("age");
                    indivGender = patient.getString("gender");
                    // Background node is JSON Object within the data array.
                    background = data.getJSONObject("background");

                    assessment = data.getJSONObject("assessment");

                    vitals = assessment.getJSONObject("vitals");
                    withIndwellingCatheter = assessment.getJSONObject("withindwelling");
                    withoutIndwellingCatheter = assessment.getJSONObject("withoutindwelling");
                    labs = assessment.getJSONObject("labs");

                    ReviewOutputJSONoptions();


                } catch (final JSONException e) {
                    Log.e(TAG, "Json parsing error: " + e.getMessage());
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(),
                                    "Could not Retrieve SBAR details: " + e.getMessage(),
                                    Toast.LENGTH_LONG).show();
                        }
                    });
                }
            }

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);

            TextView resultsDate, resultsPatientGender, resultsPatientAge, resultsCath,
                    resultsIncontinence, resultsUTI6, resultsPyelone, resultsProst, resultsAllergy,
                    resultsNotesOrganism, resultsNotesTreatment, resultsNotesDiagnosis, resultsNotesDirectives,
                    resultsBpLow, resultsBpHigh, resultsHr, resultsRespRate, resultsTemp, resultsO2,
                    withORwithout,
                    resultAssess1, resultAssess2, resultAssess3, resultAssess4, resultAssess5, resultAssess6, resultAssess7,
                    resultAssess8, resultAssess9;

            resultsDate = findViewById(R.id.result_date);
            resultsPatientGender = findViewById(R.id.result_patient_gender);
            resultsPatientAge = findViewById(R.id.result_patient_age);

            resultsCath = findViewById(R.id.result_background_1);
            resultsIncontinence = findViewById(R.id.result_background_2);
            resultsUTI6 = findViewById(R.id.result_background_3);
            resultsPyelone = findViewById(R.id.result_background_4);
            resultsProst = findViewById(R.id.result_background_5);
            resultsAllergy = findViewById(R.id.result_background_6);

            resultsNotesOrganism = findViewById(R.id.nurse_notes_1);
            resultsNotesTreatment = findViewById(R.id.nurse_notes_2);
            resultsNotesDiagnosis = findViewById(R.id.nurse_notes_3);
            resultsNotesDirectives = findViewById(R.id.nurse_notes_4);

            resultsBpLow = findViewById(R.id.vitals_1);
            resultsBpHigh = findViewById(R.id.vitals_2);
            resultsHr = findViewById(R.id.vitals_3);
            resultsRespRate = findViewById(R.id.vitals_4);
            resultsTemp = findViewById(R.id.vitals_5);
            resultsO2 = findViewById(R.id.vitals_6);

            withORwithout = findViewById(R.id.result_catheter_assessment);
            resultAssess1 = findViewById(R.id.result_catheter_1);
            resultAssess2 = findViewById(R.id.result_catheter_2);
            resultAssess3 = findViewById(R.id.result_catheter_3);
            resultAssess4 = findViewById(R.id.result_catheter_4);
            resultAssess5 = findViewById(R.id.result_catheter_5);
            resultAssess6 = findViewById(R.id.result_catheter_6);
            resultAssess7 = findViewById(R.id.result_catheter_7);
            resultAssess8 = findViewById(R.id.result_catheter_8);
            resultAssess9 = findViewById(R.id.result_catheter_9);

            TextView titlePatientID = findViewById(R.id.get_id);
            titlePatientID.setText(selectedID);
            resultsDate.setText(indivDate);
            resultsPatientGender.setText("Gender - " + indivGender);
            resultsPatientAge.setText("Age - " + indivAge);

            resultsCath.setText(indivCatheter);
            resultsIncontinence.setText(indivIncontinence);
            resultsUTI6.setText(indivUTI6);
            resultsPyelone.setText(indivPyelonephritis);
            resultsProst.setText(indivProstatitis);
            resultsAllergy.setText(indivPenicillinAllergy);

            resultsNotesOrganism.setText(indivNurseNoteOrganisms);
            resultsNotesTreatment.setText(indivNurseNoteTreatment);
            resultsNotesDiagnosis.setText(indivNurseNoteDiagnosis);
            resultsNotesDirectives.setText(indivNurseNoteDirectives);

            resultsBpLow.setText(indivBpLow);
            resultsBpHigh.setText(indivBpHigh);
            resultsHr.setText(indivHr);
            resultsRespRate.setText(indivRespRate);
            resultsTemp.setText(indivTemp);
            resultsO2.setText(indivO2);

            withORwithout.setText(withORwithoutCath);
            resultAssess1.setText(assess1);
            resultAssess2.setText(assess2);
            resultAssess3.setText(assess3);
            resultAssess4.setText(assess4);
            resultAssess5.setText(assess5);
            resultAssess6.setText(assess6);
            resultAssess7.setText(assess7);
            resultAssess8.setText(assess8);
            resultAssess9.setText(assess9);

        }
    }

    public void ReviewOutputJSONoptions() {
        try {
            //Background Outputs
            if (background.has("indwelling catheter")) {
                indivCatheter = "Indwelling Catheter";
            }
            if (background.has("incontinence")) {
                indivIncontinence = "Incontinent";
            }
            if (background.has("uti6month")) {
                indivUTI6 = "Recent UTI (6m)";
            }
            if (background.has("pyelonephritis")) {
                indivPyelonephritis = "Peylonephritis";
            }
            if (background.has("prostatitis")) {
                indivProstatitis = "Prostatitis";
            }
            if (background.has("penicillinallergy")) {
                indivPenicillinAllergy = "B Lactem Allergy";
            }


            //Nurse Notes Outputs
            if (background.has("uti6organism")) {
                indivNurseNoteOrganisms = background.getString("uti6organism");
            }
            if (background.has("uti6treatment")) {
                indivNurseNoteTreatment = background.getString("uti6treatment");
            }
            if (background.has("diagnosis")) {
                indivNurseNoteDiagnosis = background.getString("diagnosis");
            }
            if (background.has("directives")) {
                indivNurseNoteDirectives = background.getString("directives");
            }


            //Vitals Outputs
            if (vitals.has("weight")) {
                indivWeight = vitals.getString("weight");
            }
            if (vitals.has("bplow")) {
                indivBpLow = vitals.getString("bplow");
            }
            if (vitals.has("bphigh")) {
                indivBpHigh = vitals.getString("bphigh");
            }
            if (vitals.has("hr")) {
                indivHr = vitals.getString("hr");
            }
            if (vitals.has("resprate")) {
                indivRespRate = vitals.getString("resprate");
            }
            if (vitals.has("temp")) {
                indivTemp = vitals.getString("temp");
            }
            if (vitals.has("o2sats")) {
                indivO2 = vitals.getString("o2sats");
            }

            //Lab Results
            if (labs.has("serumcreatinine")) {
                indivSerumCreatinine = labs.getString("serumcreatinine");
            }

            //Catheter Assessments - with
            if (withIndwellingCatheter.length() > 0) {

                withORwithoutCath = "Indwelling Catheter";
                assess8 = "";
                assess9 = "";

                if (withIndwellingCatheter.has("fever100repeat99")) {
                    assess1 = "Fever of 100F or repeated 99F";
                }
                if (withIndwellingCatheter.has("backpain")) {
                    assess2 = "New Back or Flank Pain";
                }
                if (withIndwellingCatheter.has("shakes")) {
                    assess3 = "Rigor/Shaking/Chills";
                }
                if (withIndwellingCatheter.has("delirium")) {
                    assess4 = "New Onset Delirium";
                }
                if (withIndwellingCatheter.has("hypertension")) {
                    assess5 = "Hypertension(Sig change in Baseline BP)";
                }
                if (withIndwellingCatheter.has("suprapubic")) {
                    assess6 = "Acute Suprapubic Pain";
                }
                if (withIndwellingCatheter.has("scrotalswelling")) {
                    assess7 = "Swelling/Tenderness of Scrotal Area";
                }
                //Catheter Assessments - without
            } else if (withoutIndwellingCatheter.length() > 0) {
                withORwithoutCath = "NO Indwelling Catheter";

                if (withoutIndwellingCatheter.has("dysuria")) {
                    assess1 = "Acute Dysuria alone";
                } else if (withoutIndwellingCatheter.has("scrotalTenderness")) {
                    assess1 = "Swelling or Tenderness of Scrotal Area";
                }

                if (withoutIndwellingCatheter.has("criteria2")) {
                    assess2 = "Temp of 100F or 2F above baseline, and the following:";
                    if (withoutIndwellingCatheter.has("urgencyCriteria2")) {
                        assess3 = "Urgency";
                    }
                    if (withoutIndwellingCatheter.has("frequencyCriteria2")) {
                        assess4 = "Frequency";
                    }
                    if (withoutIndwellingCatheter.has("backpainCriteria2")) {
                        assess5 = "Back or Flank Pain";
                    }
                    if (withoutIndwellingCatheter.has("suprapubicCriteria2")) {
                        assess6 = "Suprapubic Pain";
                    }
                    if (withoutIndwellingCatheter.has("hematuriaCriteria2")) {
                        assess7 = "Gross Hematuria";
                    }
                    if (withoutIndwellingCatheter.has("incontinenceCriteria2")) {
                        assess8 = "Urinary Incontinence";
                    }
                    if (withoutIndwellingCatheter.has("dementia")) {
                        assess9 = "Severe Dementia";
                    }

                } else if (withoutIndwellingCatheter.has("criteria3")) {
                    assess2 = "NO Fever but the below symptoms";
                    assess9 = "";
                    if (withoutIndwellingCatheter.has("urgencyCriteria3")) {
                        assess3 = "Urgency";
                    }
                    if (withoutIndwellingCatheter.has("frequencyCriteria3")) {
                        assess4 = "Frequency";
                    }
                    if (withoutIndwellingCatheter.has("backpainCriteria3")) {
                        assess5 = "Back or Flank Pain";
                    }
                    if (withoutIndwellingCatheter.has("suprapubicCriteria3")) {
                        assess6 = "Suprapubic Pain";
                    }
                    if (withoutIndwellingCatheter.has("hematuriaCriteria3")) {
                        assess7 = "Gross Hematuria";
                    }
                    if (withoutIndwellingCatheter.has("incontinenceCriteria3")) {
                        assess8 = "Urinary Incontinence";
                    }
                }

            } else {
                withORwithoutCath = "NO Catheter Info";
            }

        } catch (final JSONException e) {
            Log.e(TAG, "Json Key/Value parsing error: " + e.getMessage());
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Toast.makeText(getApplicationContext(),
                            "Could not Retrieve SBAR details: " + e.getMessage(),
                            Toast.LENGTH_LONG).show();
                }
            });
        }
    }

    public void PhysicianRecommendation () {
        setContentView(R.layout.physician3_recommendation);
        buttonBack = findViewById(R.id.back_review);
        buttonNext = findViewById(R.id.next_button);

        final RadioButton urinalysis, cranjuice, fluidintake, vitals, antibiotic;
        urinalysis = findViewById(R.id.check_urinalysis);
        cranjuice = findViewById(R.id.check_cranjuice);
        fluidintake = findViewById(R.id.check_fluid_intake);
        vitals = findViewById(R.id.check_vitals);
        antibiotic = findViewById(R.id.check_antibiotic);

        //Back button to restart physician workflow
        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                PhysicianSBARreview();
            }
        });

        //Back button to restart physician workflow
        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (urinalysis.isChecked() || cranjuice.isChecked() || fluidintake.isChecked() || vitals.isChecked()) {
                    Toast.makeText(getApplicationContext(), "No Antibiotics Needed. Contact Nurse with Instruction.", Toast.LENGTH_LONG).show();
                    onBackPressed();
                } else if (antibiotic.isChecked()) {
                    Toast.makeText(getApplicationContext(), "Predictive Analysis", Toast.LENGTH_LONG).show();
                    AntibioticRecommendation();
                } else {
                    Toast.makeText(getApplicationContext(), "Please select one of the Instructions", Toast.LENGTH_LONG).show();
                }

            }
        });

    }

    public void AntibioticRecommendation () {
        setContentView(R.layout.physician4_antibiotics);
        buttonBack = findViewById(R.id.back_review);
        buttonSubmit = findViewById(R.id.submit_button);
        buttonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });

        /*
        Our CrCl (Creatinine Clearance) calculation is calculated using a randomizer...the reason for this:
        FHIR/MIMIC data shows the serum creatinine values all at 1mg/dl which would not provide an
        adequate variation for our proof of concept.
        Given a real time patient info database, we would have programmed the following equation:

        if (gender == "male"){
            CrCl = ((140 - Age) * Weight)/(72*sCr) --sCr -> Serum Creatinine
        } else if (gender == "female") {
            CrCl = (((140 - Age) * Weight)/(72*sCr)) * 0.85
        }

        */

        float CrCl = 1 + (float)(Math.random() * ((75 - 15) + 1));
        System.out.print("CrCl: " + CrCl);
        //Drug Selection
        TextView selectDrug = findViewById(R.id.entryDrug);
        String drug = "Nitrofurantoin";
        if (CrCl > 30) {
            drug = "Nitrofurantoin";
            selectDrug.setText(drug);
        } else {
            drug = "Doxycycline";
            selectDrug.setText(drug);
        }
        //Dosage
        TextView selectDose = findViewById(R.id.entryDose);
        String dose = "100 mg";
        if (drug == "Nitrofurantoin") {
            dose = "100 mg";
            selectDose.setText(dose);
        } else if (drug == "Cephalexin") {
            dose = "500 mg";
            selectDose.setText(dose);
        } else if(drug == "Doxycycline") {
            dose = "100 mg";
            selectDose.setText(dose);
        }
        //Frequency
        TextView selectFrequency = findViewById(R.id.BID);
        String freq = "BID";
        if (drug == "Nitrofurantoin") {
            freq = "BID";
            selectFrequency.setText(freq);
        } else if (drug == "Cephalexin") {
            if (CrCl < 10) {
                freq = "Once daily";
                selectFrequency.setText(freq);
            } else if (CrCl > 10 & CrCl < 50 ) {
                freq = "TID";
                selectFrequency.setText(freq);
            } else {
                freq = "BID";
                selectFrequency.setText(freq);
            }
        } else if(drug == "Doxycycline") {
            freq = "BID";
            selectFrequency.setText(freq);
        }


    }
}

