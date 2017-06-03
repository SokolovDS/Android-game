package com.example.daniil.catchme;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.content.ContextCompat;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;


public class maps extends FragmentActivity implements OnMapReadyCallback {
    private static final int MY_LOCATION_REQUEST_CODE = 1;

    private GoogleMap mMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        double latitude = 0;
        double longitude = 0;

        Intent getuid = getIntent();
        String uid = getuid.getStringExtra("uid");
        Toast toast = Toast.makeText(getApplicationContext(), uid, Toast.LENGTH_SHORT);
        toast.show();

        // Add a marker in Sydney and move the camera
        LatLng urfu = new LatLng(56.843980, 60.653513);
        mMap.addMarker(new MarkerOptions().position(urfu).title("Marker in URFU"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(urfu));
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            mMap.setMyLocationEnabled(true);
            LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
            Criteria criteria = new Criteria();
            String provider = locationManager.getBestProvider(criteria, true);
            // Getting Current Location
            Location location = locationManager.getLastKnownLocation(provider);
            latitude = location.getLatitude();
            longitude = location.getLongitude();
            if (location != null)
            {
                latitude = location.getLatitude();
                longitude = location.getLongitude();
            }
        } else {
            // Show rationale and request permission.
        }


        //Определение местоположения

        //---------------------------------
        //Отправка запроса на получение расстояния
        RequestQueue queue = Volley.newRequestQueue(maps.this);
        String url = "http://artkholl.pythonanywhere.com/get_coord?idd="+uid.substring(1,6)+"&coord="+latitude+"$"+longitude;
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                // TODO Auto-generated method stub
                Toast toast = Toast.makeText(getApplicationContext(), response, Toast.LENGTH_SHORT);
                toast.show();
            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                // TODO Auto-generated method stub
                Toast toast = Toast.makeText(getApplicationContext(), "ERROR", Toast.LENGTH_SHORT);
                toast.show();

            }
        });
        queue.add(stringRequest);

        //----------------------------
    }

}
