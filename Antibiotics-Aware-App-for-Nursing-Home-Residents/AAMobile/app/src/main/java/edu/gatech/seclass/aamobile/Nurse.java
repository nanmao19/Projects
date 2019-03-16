package edu.gatech.seclass.aamobile;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListAdapter;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.SimpleAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.DataOutputStream;
import java.io.Serializable;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Random;


public class Nurse extends AppCompatActivity implements Serializable {

    private static final String TAG = "NurseWorkFlow";

    private Spinner mSpinnerID;
    private String resident;
    FhirActivity mimic = new FhirActivity();
    private List<String> patientList = new ArrayList();
    //N2 - Intro
    private TextView mDisplayDate;
    private DatePickerDialog.OnDateSetListener mDateSetListener;
    private EditText mOrganisms, mTreatment, mDiagnosis, mDirectives;
    private CheckBox checkUTIconcern;
    private RadioButton  checkMale, checkFemale;
    private String utiConcern, gender;
    //Checkboxes - N3 - Background
    private CheckBox checkWithCatheter, checkIncontinence, checkUTI6, checkLactemAllergy, checkPyelonephritis, checkProstatitis;
    private String wCatheter, incontinence, uti6months, lactemallergy, pyelonephritis, prostatitis;
    private RadioGroup indwellingRadioGroup;
    private RadioGroup incontinenceRadioGroup;
    private String Organisms, Treatment, Diagnosis, Directives;
    //Vitals Int Decimal Inputs
    private EditText bpLow, bpHigh, heartRate, respRate, Temp, o2Sats, weight;
    private String lowBpInput, highBpInput, heartRateInput, respRateInput, tempInput, o2Input, weightInput;
    //Checkboxes - N4 - Indwelling Catheter Options
    private CheckBox checkFever, checkBackPain, checkRigorShaking, checkDelirium, checkHypertension, checkSuprapubicPain, checkScrotalSwelling;
    private String fever, backPain, rigorShake, delirium, hypertension, suprapubicPain, scrotalSwell;
    //Checkboxes - N5 - Without Indwelling Catheter Options
    private CheckBox checkCriteria1;
    private CheckBox checkDysuria, checkTenderness;
    private String criteria1, dysuria, tenderness;

    private CheckBox checkCriteria2;
    private CheckBox checkUrgency2, checkFrequency2, checkBackPain2, checkSuprapubicPain2, checkHematuria2, checkIncontinence2, checkDementia;
    private String criteria2, urgency2, frequency2, backPain2, suprapubicPain2, hematuria2, incontinence2, dementia;

    private CheckBox checkCriteria3;
    private CheckBox checkUrgency3, checkFrequency3, checkBackPain3, checkSuprapubicPain3, checkHematuria3, checkIncontinence3;
    private String criteria3, urgency3, frequency3, backPain3, suprapubicPain3, hematuria3, incontinence3;

    //Common Buttons
    private Button buttonClear;
    private Button buttonNext;
    private Button buttonBack;
    private Button buttonHome;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.nurse1_sbaroptions);

        Button buttonExisting = findViewById(R.id.existing_button);
        Button buttonNewSBAR = findViewById(R.id.submitnew_button);
        Button buttonLogout = findViewById(R.id.logout_button);

        // click Review existing SBAR button
        buttonExisting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ReviewExistingSBAR();
            }
        });

        // click submit new SBAR button
        buttonNewSBAR.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Must wait until pulling FHIR/MIMIC Data is complete.
                new GetFHIRserverPatients().execute();

            }
        });

        // click Logout button
        buttonLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(i);
            }
        });
    }

    public class GetFHIRserverPatients extends AsyncTask<Void, Void, Void> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Toast.makeText(Nurse.this, "Loading FHIR/MIMIC Patients. Please Wait...", Toast.LENGTH_LONG).show();
        }

        @Override
        protected Void doInBackground(Void... arg0) {
            patientList = mimic.getPatients();

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            SubmitSBAR();
        }
    }

    // back button works here
    @Override
    public void onBackPressed() {
        Intent i = new Intent(this, Nurse.class);
        startActivity(i);
    }

    //Three main SBAR entry screens
    public void ReviewExistingSBAR() {
        setContentView(R.layout.nurse_existing_sbars);

        buttonHome = findViewById(R.id.home_review_button);

        buttonHome.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });

        Intent i = new Intent(this, JsonUtilNurse.class);
        startActivity(i);

    }


    public void SubmitSBAR() {
        setContentView(R.layout.nurse2_sbar_intro);

        checkUTIconcern = findViewById(R.id.uti_concern);
        checkMale = findViewById(R.id.gender_male);
        checkFemale = findViewById(R.id.gender_female);
        buttonNext = findViewById(R.id.next_button);
        buttonBack = findViewById(R.id.back_situation);

        // Pull unique patients list from MIMIC, only the patients with serum Creatinine LOINC codes applicable.
        mSpinnerID = findViewById(R.id.spinner_resident_id);
        ArrayAdapter<String> residAdapter = new ArrayAdapter<>(Nurse.this,
                R.layout.support_simple_spinner_dropdown_item, patientList);

        mSpinnerID.setAdapter(residAdapter);

        mSpinnerID.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                resident = (String) parent.getItemAtPosition(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                //Not Applicable
            }
        });


        // click next button to proceed
        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkUTIconcern.isChecked()) {
                    collectCheckBoxAnswers();
                    backgroundEntry();
                } else {
                    Toast.makeText(getApplicationContext(), "Antibiotic Prescription May NOT be needed. Consult Physician.", Toast.LENGTH_LONG).show();
                }
            }
        });
        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });
    }


    //Supplementary Methods
    public void backgroundEntry() {

        setContentView(R.layout.nurse3_sbar_backgroundinput);

        buttonClear = findViewById(R.id.clear_button);
        buttonNext = findViewById(R.id.next_button);
        buttonHome = findViewById(R.id.home_background);
        checkWithCatheter = findViewById(R.id.interdwellingCathetar);
        checkIncontinence = findViewById(R.id.incontinence);
        indwellingRadioGroup = findViewById(R.id.indwellingRadio);
        incontinenceRadioGroup = findViewById(R.id.incontinenceRadio);
        checkUTI6 = findViewById(R.id.utiIn6);

        mOrganisms = findViewById(R.id.organisms);
        mTreatment = findViewById(R.id.treatment);
        mDiagnosis = findViewById(R.id.active_diagnosis);
        mDirectives = findViewById(R.id.advance_directives);
        checkLactemAllergy = findViewById(R.id.blactemallergy);
        checkPyelonephritis = findViewById(R.id.pyelonephritis);
        checkProstatitis = findViewById(R.id.prostatitis);

        getAndSetDate();

//Activate Radio button only if Indwelling Catheter is checked
        final RadioGroup rg1 = indwellingRadioGroup;
        CheckBox ck1 = checkWithCatheter;
        ck1.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton ck1, boolean checked) {
                //basically, since we will set enabled state to whatever state the checkbox is
                //therefore, we will only have to setEnabled(checked)
                for (int i = 0; i < rg1.getChildCount(); i++) {
                    (rg1.getChildAt(i)).setEnabled(checked);
                }
            }
        });
//set default to false
        for (int i = 0; i < rg1.getChildCount(); i++) {
            (rg1.getChildAt(i)).setEnabled(false);
        }

//Activate Radio button only if Incontinence is checked
        final RadioGroup rg2 = incontinenceRadioGroup;
        CheckBox ck2 = checkIncontinence;
        ck2.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton ck2, boolean checked) {
                //basically, since we will set enabled state to whatever state the checkbox is
                //therefore, we will only have to setEnabled(checked)
                for (int i = 0; i < rg2.getChildCount(); i++) {
                    (rg2.getChildAt(i)).setEnabled(checked);
                }
            }
        });
//set default to false
        for (int i = 0; i < rg2.getChildCount(); i++) {
            (rg2.getChildAt(i)).setEnabled(false);
        }


        // click clear button clears all check marks and resets date.
        buttonClear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                getAndSetDate();
                clearCheckBoxes();
                mOrganisms.getText().clear();
                mTreatment.getText().clear();
                mDiagnosis.getText().clear();
                mDirectives.getText().clear();
                indwellingRadioGroup.clearCheck();
                incontinenceRadioGroup.clearCheck();
            }
        });

        // click next button moves forward to vitals input for Nurse Workflow
        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                saveNurseNotes();
                collectCheckBoxAnswers();
                vitals();
            }
        });

        buttonHome.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });
    }

    public void vitals() {
        setContentView(R.layout.nurse3b_sbar_vitalsinput);

        buttonNext = findViewById(R.id.next_button_vitals);
        buttonClear = findViewById(R.id.clear_button_vitals);
        buttonBack = findViewById(R.id.back_button_vitals);

        bpLow = findViewById(R.id.bplow);
        bpHigh = findViewById(R.id.bphigh);
        heartRate = findViewById(R.id.hr);
        respRate = findViewById(R.id.resprate);
        Temp = findViewById(R.id.temp);
        o2Sats = findViewById(R.id.o2sats);
        weight = findViewById(R.id.weightint);

        // click clear button clears all inputted vitals.
        buttonClear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                bpLow.getText().clear();
                bpHigh.getText().clear();
                heartRate.getText().clear();
                respRate.getText().clear();
                Temp.getText().clear();
                o2Sats.getText().clear();
                weight.getText().clear();
            }
        });


        // click next button can result in two screens for Nurse Workflow
        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkWithCatheter.isChecked()) {
                    saveVitals();
                    indwellingCatheter();
                } else {
                    saveVitals();
                    noIndwellingCatheter();
                }
            }
        });

        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });

    }

    // Method for Indewelling Catheter Scenario.
    public void indwellingCatheter() {
        setContentView(R.layout.nurse4_with_indwelling_cath);

        buttonNext = findViewById(R.id.next_2);
        buttonClear = findViewById(R.id.clear_2);
        buttonBack = findViewById(R.id.back_2);

        checkFever = findViewById(R.id.fever);
        checkBackPain = findViewById(R.id.pain);
        checkRigorShaking = findViewById(R.id.chills);
        checkDelirium = findViewById(R.id.delirium);
        checkHypertension = findViewById(R.id.tension);
        checkSuprapubicPain = findViewById(R.id.suprapubic_pain);
        checkScrotalSwelling = findViewById(R.id.scrotal);

        // click next button to proceed
        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkFever.isChecked() || checkBackPain.isChecked() || checkRigorShaking.isChecked() ||
                        checkDelirium.isChecked() || checkHypertension.isChecked() ||
                        checkSuprapubicPain.isChecked() || checkScrotalSwelling.isChecked()) {
                    collectCheckBoxAnswers();
                    sbarRecommendation(1);
                } else {
                    collectCheckBoxAnswers();
                    sbarRecommendation(2);
                }
            }
        });
        buttonClear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                clearCheckBoxes();
            }
        });
        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                backgroundEntry();
            }
        });

    }

    // Method for NO Indwelling Catheter Scenario.
    public void noIndwellingCatheter() {
        setContentView(R.layout.nurse5_without_indwelling_cath);

        buttonNext = findViewById(R.id.next_without);
        buttonBack = findViewById(R.id.back_without);
        buttonClear = findViewById(R.id.clear_without);

        checkCriteria1 = findViewById(R.id.without_1);
        checkDysuria = findViewById(R.id.dysuria);
        checkTenderness = findViewById(R.id.tenderness);
        checkCriteria2 = findViewById(R.id.without_2);
        checkUrgency2 = findViewById(R.id.urgency);
        checkFrequency2 = findViewById(R.id.frequency_2);
        checkBackPain2 = findViewById(R.id.back_pain);
        checkSuprapubicPain2 = findViewById(R.id.Suprapubic);
        checkHematuria2 = findViewById(R.id.hematuria_2);
        checkIncontinence2 = findViewById(R.id.incontinence);
        checkDementia = findViewById(R.id.dimentia);
        checkCriteria3 = findViewById(R.id.without_3);
        checkUrgency3 = findViewById(R.id.urgency_2);
        checkFrequency3 = findViewById(R.id.frequency_3);
        checkBackPain3 = findViewById(R.id.back_pain_3);
        checkSuprapubicPain3 = findViewById(R.id.suprapubic_3);
        checkHematuria3 = findViewById(R.id.hematuria_3);
        checkIncontinence3 = findViewById(R.id.incontinence_3);

        buttonNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkCriteria1.isChecked() || checkCriteria2.isChecked() ||
                        checkCriteria3.isChecked()) {
                    collectCheckBoxAnswers();
                    sbarRecommendation(1);
                } else {
                    collectCheckBoxAnswers();
                    sbarRecommendation(2);
                }
            }
        });

        buttonClear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                clearCheckBoxes();
            }
        });
        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                backgroundEntry();
            }
        });
    }

    public void sbarRecommendation(int option) {
        setContentView(R.layout.nurse6_sbar_recommendation);
        buttonBack = findViewById(R.id.back_recommendation);
        Button buttonSubmit = findViewById(R.id.submitfinal_button);

        if (option == 1) {
            CheckBox cb1 = findViewById(R.id.recommendation1);
            CheckBox cb2 = findViewById(R.id.recommendation2);
            cb1.setChecked(!cb1.isChecked());
            cb2.setEnabled(false);
        } else {
            CheckBox cb1 = findViewById(R.id.recommendation1);
            CheckBox cb2 = findViewById(R.id.recommendation2);
            cb1.setEnabled(false);
            cb2.setChecked(!cb2.isChecked());

        }

        buttonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                backgroundEntry();
            }
        });

        buttonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                convertDataToJSON();
                Toast.makeText(getApplicationContext(), "Thank you! Your SBAR has been submitted to a Physician for review.", Toast.LENGTH_LONG).show();
                onBackPressed();
            }
        });
    }

    //Save Nurse Notes to String
    public void saveNurseNotes() {
        Organisms = mOrganisms.getText().toString();
        Treatment = mTreatment.getText().toString();
        Diagnosis = mDiagnosis.getText().toString();
        Directives = mDirectives.getText().toString();
    }

    public void saveVitals() {
        lowBpInput = bpLow.getText().toString();
        highBpInput = bpHigh.getText().toString();
        heartRateInput = heartRate.getText().toString();
        respRateInput = respRate.getText().toString();
        tempInput = Temp.getText().toString();
        o2Input = o2Sats.getText().toString();
        weightInput = weight.getText().toString();
    }

    //Get and Set dates
    public void getAndSetDate() {
        mDisplayDate = findViewById(R.id.display_date);
        mDisplayDate.setText("SELECT DATE");

        mDisplayDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Calendar cal = Calendar.getInstance();
                int year = cal.get(Calendar.YEAR);
                int month = cal.get(Calendar.MONTH);
                int day = cal.get(Calendar.DAY_OF_MONTH);

                DatePickerDialog dialog = new DatePickerDialog(
                        Nurse.this,
                        android.R.style.Theme_Holo_Light_Dialog_MinWidth,
                        mDateSetListener,
                        year, month, day);
                dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
                dialog.show();
            }
        });

        mDateSetListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int year, int month, int day) {
                month = month + 1;
                Log.d(TAG, "onDateSet: mm-dd-yyyy: " + month + "-" + day + "-" + year);

                String date = month + "-" + day + "-" + year;
                mDisplayDate.setText(date);
            }
        };
    }


    public void clearCheckBoxes() {
        if ((checkWithCatheter != null) && checkWithCatheter.isChecked()) {
            checkWithCatheter.setChecked(false);
        }
        if ((checkIncontinence != null) && checkIncontinence.isChecked()) {
            checkIncontinence.setChecked(false);
        }
        if ((checkUTI6 != null) && checkUTI6.isChecked()) {
            checkUTI6.setChecked(false);
        }
        if ((checkLactemAllergy != null) && checkLactemAllergy.isChecked()) {
            checkLactemAllergy.setChecked(false);
        }
        if ((checkPyelonephritis != null) && checkPyelonephritis.isChecked()) {
            checkPyelonephritis.setChecked(false);
        }
        if ((checkProstatitis != null) && checkProstatitis.isChecked()) {
            checkProstatitis.setChecked(false);
        }

        if ((checkFever != null) && checkFever.isChecked()) {
            checkFever.setChecked(false);
        }
        if ((checkBackPain != null) && checkBackPain.isChecked()) {
            checkBackPain.setChecked(false);
        }
        if ((checkRigorShaking != null) && checkRigorShaking.isChecked()) {
            checkRigorShaking.setChecked(false);
        }
        if ((checkDelirium != null) && checkDelirium.isChecked()) {
            checkDelirium.setChecked(false);
        }
        if ((checkHypertension != null) && checkHypertension.isChecked()) {
            checkHypertension.setChecked(false);
        }
        if ((checkSuprapubicPain != null) && checkSuprapubicPain.isChecked()) {
            checkSuprapubicPain.setChecked(false);
        }
        if ((checkScrotalSwelling != null) && checkScrotalSwelling.isChecked()) {
            checkScrotalSwelling.setChecked(false);
        }
        //Criteria 1 checkboxes for w/o indwelling catheter.
        if ((checkCriteria1 != null) && checkCriteria1.isChecked()) {
            checkCriteria1.setChecked(false);
        }
        if ((checkDysuria != null) && checkDysuria.isChecked()) {
            checkDysuria.setChecked(false);
        }
        if ((checkTenderness != null) && checkTenderness.isChecked()) {
            checkTenderness.setChecked(false);
        }

        //Criteria 2 checkboxes for w/o indwelling catheter.
        if ((checkCriteria2 != null) && checkCriteria2.isChecked()) {
            checkCriteria2.setChecked(false);
        }
        if ((checkUrgency2 != null) && checkUrgency2.isChecked()) {
            checkUrgency2.setChecked(false);
        }
        if ((checkFrequency2 != null) && checkFrequency2.isChecked()) {
            checkFrequency2.setChecked(false);
        }
        if ((checkBackPain2 != null) && checkBackPain2.isChecked()) {
            checkBackPain2.setChecked(false);
        }
        if ((checkSuprapubicPain2 != null) && checkSuprapubicPain2.isChecked()) {
            checkSuprapubicPain2.setChecked(false);
        }
        if ((checkHematuria2 != null) && checkHematuria2.isChecked()) {
            checkHematuria2.setChecked(false);
        }
        if ((checkIncontinence2 != null) && checkIncontinence2.isChecked()) {
            checkIncontinence2.setChecked(false);
        }
        if ((checkDementia != null) && checkDementia.isChecked()) {
            checkDementia.setChecked(false);
        }

        //Criteria 3 checkboxes for w/o indwelling catheter.
        if ((checkCriteria3 != null) && checkCriteria3.isChecked()) {
            checkCriteria3.setChecked(false);
        }
        if ((checkUrgency3 != null) && checkUrgency3.isChecked()) {
            checkUrgency3.setChecked(false);
        }
        if ((checkFrequency3 != null) && checkFrequency3.isChecked()) {
            checkFrequency3.setChecked(false);
        }
        if ((checkBackPain3 != null) && checkBackPain3.isChecked()) {
            checkBackPain3.setChecked(false);
        }
        if ((checkSuprapubicPain3 != null) && checkSuprapubicPain3.isChecked()) {
            checkSuprapubicPain3.setChecked(false);
        }
        if ((checkHematuria3 != null) && checkHematuria3.isChecked()) {
            checkHematuria3.setChecked(false);
        }
        if ((checkIncontinence3 != null) && checkIncontinence3.isChecked()) {
            checkIncontinence3.setChecked(false);
        }
    }

    public void collectCheckBoxAnswers() {
        if ((checkUTIconcern != null) && checkUTIconcern.isChecked()) {
            utiConcern = "Yes";
        }
        if ((checkMale != null) && checkMale.isChecked()) {
            gender = "male";
        } else if (checkFemale!= null && checkFemale.isChecked()) {
            gender = "female";
        }
        if ((checkWithCatheter != null) && checkWithCatheter.isChecked()) {
            wCatheter = "Yes";
        }
        if ((checkIncontinence != null) && checkIncontinence.isChecked()) {
            incontinence = "Yes";
        }
        if ((checkUTI6 != null) && checkUTI6.isChecked()) {
            uti6months = "Yes";
        }
        if ((checkLactemAllergy != null) && checkLactemAllergy.isChecked()) {
            lactemallergy = "Yes";
        }
        if ((checkPyelonephritis != null) && checkPyelonephritis.isChecked()) {
            pyelonephritis = "Yes";
        }
        if ((checkLactemAllergy != null) && checkLactemAllergy.isChecked()) {
            prostatitis = "Yes";
        }
        if ((checkFever != null) && checkFever.isChecked()) {
            fever = "Yes";
        }
        if ((checkBackPain != null) && checkBackPain.isChecked()) {
            backPain = "Yes";
        }
        if ((checkRigorShaking != null) && checkRigorShaking.isChecked()) {
            rigorShake = "Yes";
        }
        if ((checkDelirium != null) && checkDelirium.isChecked()) {
            delirium = "Yes";
        }
        if ((checkHypertension != null) && checkHypertension.isChecked()) {
            hypertension = "Yes";
        }
        if ((checkSuprapubicPain != null) && checkSuprapubicPain.isChecked()) {
            suprapubicPain = "Yes";
        }
        if ((checkScrotalSwelling != null) && checkScrotalSwelling.isChecked()) {
            scrotalSwell = "Yes";
        }
        //Criteria 1 checkboxes for w/o indwelling catheter.
        if ((checkCriteria1 != null) && checkCriteria1.isChecked()) {
            criteria1 = "Yes";
        }
        if ((checkDysuria != null) && checkDysuria.isChecked()) {
            dysuria = "Yes";
        }
        if ((checkTenderness != null) && checkTenderness.isChecked()) {
            tenderness = "Yes";
        }

        //Criteria 2 checkboxes for w/o indwelling catheter.
        if ((checkCriteria2 != null) && checkCriteria2.isChecked()) {
            criteria2 = "Yes";
        }
        if ((checkUrgency2 != null) && checkUrgency2.isChecked()) {
            urgency2 = "Yes";
        }
        if ((checkFrequency2 != null) && checkFrequency2.isChecked()) {
            frequency2 = "Yes";
        }
        if ((checkBackPain2 != null) && checkBackPain2.isChecked()) {
            backPain2 = "Yes";
        }
        if ((checkSuprapubicPain2 != null) && checkSuprapubicPain2.isChecked()) {
            suprapubicPain2 = "Yes";
        }
        if ((checkHematuria2 != null) && checkHematuria2.isChecked()) {
            hematuria2 = "Yes";
        }
        if ((checkIncontinence2 != null) && checkIncontinence2.isChecked()) {
            incontinence2 = "Yes";
        }
        if ((checkDementia != null) && checkDementia.isChecked()) {
            dementia = "Yes";
        }

        //Criteria 3 checkboxes for w/o indwelling catheter.
        if ((checkCriteria3 != null) && checkCriteria3.isChecked()) {
            criteria3 = "Yes";
        }
        if ((checkUrgency3 != null) && checkUrgency3.isChecked()) {
            urgency3 = "Yes";
        }
        if ((checkFrequency3 != null) && checkFrequency3.isChecked()) {
            frequency3 = "Yes";
        }
        if ((checkBackPain3 != null) && checkBackPain3.isChecked()) {
            backPain3 = "Yes";
        }
        if ((checkSuprapubicPain3 != null) && checkSuprapubicPain3.isChecked()) {
            suprapubicPain3 = "Yes";
        }
        if ((checkHematuria3 != null) && checkHematuria3.isChecked()) {
            hematuria3 = "Yes";
        }
        if ((checkIncontinence3 != null) && checkIncontinence3.isChecked()) {
            incontinence3 = "Yes";
        }
    }

    //TODO: need to pull age, serum creatinine measurement into JSON? Done in separate activity.
    public void convertDataToJSON() {
        String url = "https://cs6440-f18-prj34.apps.hdap.gatech.edu/api/patients";
        //Main JSON
        JSONObject Combined = new JSONObject();
        JSONObject fullDataObj = new JSONObject();
        //Patient Info JSON - this will include the situation as well whether the nurse is concerned about a UTI.
        JSONObject patientInfo = new JSONObject();
        //Background info for patient JSON
        JSONObject background = new JSONObject();
        //Vitals JSON
        JSONObject vitals = new JSONObject();
        //Assessment JSONs
        JSONObject assessment = new JSONObject();
        JSONObject withIndwelling = new JSONObject();
        JSONObject withoutIndwelling = new JSONObject();
        JSONObject labs = new JSONObject();

        try {
            //Convert the Java objects into JSON.
            patientInfo.put("id", resident);
            patientInfo.put("date", mDisplayDate.getText().toString());
            patientInfo.put("gender", gender);
            patientInfo.put("uticoncern", utiConcern);

            background.put("indwelling catheter", wCatheter);
            background.put("incontinence", incontinence);
            background.put("uti6month", uti6months);
            background.put("uti6organism", Organisms);
            background.put("uti6treatment", Treatment);
            background.put("diagnosis", Diagnosis);
            background.put("directives", Directives);
            background.put("penicillinallergy", lactemallergy);
            background.put("pyelonephritis", pyelonephritis);
            background.put("prostatitis", prostatitis);

            vitals.put("weight", weightInput);
            vitals.put("bplow", lowBpInput);
            vitals.put("bphigh", highBpInput);
            vitals.put("hr", heartRateInput);
            vitals.put("resprate", respRateInput);
            vitals.put("temp", tempInput);
            vitals.put("o2sats", o2Input);

            withIndwelling.put("fever100repeat99", fever);
            withIndwelling.put("backpain", backPain);
            withIndwelling.put("shakes", rigorShake);
            withIndwelling.put("delirium", delirium);
            withIndwelling.put("hypertension", hypertension);
            withIndwelling.put("suprapubic", suprapubicPain);
            withIndwelling.put("scrotalswelling", scrotalSwell);

            withoutIndwelling.put("criteria1", criteria1);
            withoutIndwelling.put("dysuria", dysuria);
            withoutIndwelling.put("scrotalTenderness", tenderness);
            withoutIndwelling.put("criteria2", criteria2);
            withoutIndwelling.put("urgencyCriteria2", urgency2);
            withoutIndwelling.put("frequencyCriteria2", frequency2);
            withoutIndwelling.put("backpainCriteria2", backPain2);
            withoutIndwelling.put("suprapubicCriteria2", suprapubicPain2);
            withoutIndwelling.put("hematuriaCriteria2", hematuria2);
            withoutIndwelling.put("incontinenceCriteria2", incontinence2);
            withoutIndwelling.put("dementia", dementia);
            withoutIndwelling.put("criteria3", criteria3);
            withoutIndwelling.put("urgencyCriteria3", urgency3);
            withoutIndwelling.put("frequencyCriteria3", frequency3);
            withoutIndwelling.put("backpainCriteria3", backPain3);
            withoutIndwelling.put("suprapubicCriteria3", suprapubicPain3);
            withoutIndwelling.put("hematuriaCriteria3", hematuria3);
            withoutIndwelling.put("incontinenceCriteria3", incontinence3);

            //TODO: Replace serum creatinine randomizer with MIMIC Data Pull
            double serumCreatinine = 0 + new Random().nextDouble()*(2);
            DecimalFormat numberFormat = new DecimalFormat("#.00");
            String sCr = numberFormat.format(serumCreatinine);
            labs.put("serumcreatinine", sCr);

            //Add vitals JSON object into the assessment JSON object - to be populated with nurse test results
            assessment.put("vitals", vitals);
            //Add withIndwelling assessment JSON Object into the assessment JSON object
            assessment.put("withindwelling", withIndwelling);
            //Add withoutIndwellingCatheter assessment JSON Object into the assessment JSON object
            assessment.put("withoutindwelling", withoutIndwelling);
            //Add labs JSON Object into the assessment JSON object - to be populated with MIMIC/FHIR/HDAP server patient data
            assessment.put("labs", labs);

            //Add all above object structures to the main 'data' JSON
            Combined.put("patientinfo", patientInfo);
            Combined.put("background", background);
            Combined.put("assessment", assessment);

            fullDataObj.put("data", Combined);

            Log.e(TAG, "Submitted JSON: " + fullDataObj);


        } catch (JSONException e) {
            e.printStackTrace();
        }

        sendPost(url,fullDataObj);

    }


    public void sendPost(final String urlAddress, final JSONObject output) {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    URL url = new URL(urlAddress);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json");
                    conn.setRequestProperty("Accept","application/json");
                    conn.setDoOutput(true);
                    conn.setDoInput(true);


                    DataOutputStream os = new DataOutputStream(conn.getOutputStream());
                    //os.writeBytes(URLEncoder.encode(jsonParam.toString(), "UTF-8"));
                    os.writeBytes(output.toString());

                    os.flush();
                    os.close();

                    Log.i("STATUS", String.valueOf(conn.getResponseCode()));
                    Log.i("MSG" , conn.getResponseMessage());

                    conn.disconnect();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        thread.start();
    }
}
