% Mini expert system in SWI-Prolog.
% Load with: ?- [expert_system_prolog].
% Query with: ?- recommendation(X).

% Example facts (edit these to test different cases).
symptom(no_internet).
symptom(router_light_red).
% symptom(router_light_green).
% symptom(single_device_only).

recommendation(check_router_power_and_cables) :-
    symptom(no_internet),
    symptom(router_light_red).

recommendation(check_wifi_or_network_settings) :-
    symptom(no_internet),
    symptom(router_light_green).

recommendation(check_device_settings) :-
    symptom(no_internet),
    symptom(single_device_only).

recommendation(contact_internet_provider) :-
    symptom(no_internet),
    symptom(router_light_green),
    symptom(all_devices_affected).

% Catch-all advice if no specific rule is supported.
recommendation(run_general_network_checklist) :-
    \+ recommendation(check_router_power_and_cables),
    \+ recommendation(check_wifi_or_network_settings),
    \+ recommendation(check_device_settings),
    \+ recommendation(contact_internet_provider).
