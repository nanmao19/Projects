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
import android.widget.SimpleAdapter;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class JsonUtilNurse extends AppCompatActivity {

    private String TAG = JsonUtilNurse.class.getSimpleName();
    private ListView lv;
    private Button buttonHome;

    private JSONArray dataArray = new JSONArray();
    private JSONObject patient = new JSONObject();

    ArrayList<HashMap<String, String>> patientList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.nurse_existing_sbars);
        buttonHome = findViewById(R.id.home_review_button);

        patientList = new ArrayList<>();
        lv = findViewById(R.id.list);

        new GetSBARs().execute();

        clickSBAR();

        //Home button to restart physician workflow
        buttonHome.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });
    }

    // back button works here
    @Override
    public void onBackPressed() {
        Intent i = new Intent(this, Nurse.class);
        startActivity(i);
    }

    public class GetSBARs extends AsyncTask<Void, Void, Void> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Toast.makeText(JsonUtilNurse.this, "Loading Submitted SBARs", Toast.LENGTH_SHORT).show();
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
                        if (patient.has("uticoncern")){
                            uticoncern = "UTI Concern: " + patient.getString("uticoncern");
                        } else {
                            uticoncern = "N/A";
                        }

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
            ListAdapter adapter = new SimpleAdapter(JsonUtilNurse.this, patientList,
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
                String selectedItem = String.valueOf(parent.getItemAtPosition(position));

                Toast.makeText(JsonUtilNurse.this,"SBAR Selected: " + selectedItem, Toast.LENGTH_LONG).show();
            }
        });
    }
}
