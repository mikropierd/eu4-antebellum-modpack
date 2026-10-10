# Bugfixes -> Antebellum: status

Wynik nakładania patchy z grotaclasBugfixes (per plik, wszystko-albo-nic, kontekst dokładny bez fuzz).

| status | liczba |
|---|---|
| applied | 10 |
| already | 3 |
| missing | 301 |
| conflict | 11 |

- applied: nałożone
- already: poprawka już jest w pliku
- missing: pliku nie ma w tym repo (dla Antebellum: jest w bazowym modzie Ante Bellum)
- conflict: plik jest, ale hunki nie pasują dokładnie (wymaga ręcznego scalenia)


## conflict

- `0006-make-confucian-monuments-work-with-harmonized-religious-groups.patch`: `common/great_projects/01_monuments.txt`
- `0010-allow-Amsterdam-Bourse-with-roman-culture.patch`: `common/great_projects/01_monuments.txt`
- `0013-fix-Italian-Coastal-Influence-privilege.patch`: `common/estate_privileges/03_burgher_privileges.txt`
- `0020-fix-or-remove-outdated-dynamic-names-for-the-province-Dortmund69.patch`: `common/province_names/ROM.txt`
- `0028-allow-custom-nations-to-keep-livonian-reforms.patch`: `common/government_reforms/01_government_reforms_monarchies.txt`
- `0032-Allow-France-to-annex-normal-vassals-without-seizing-land.patch`: `common/diplomatic_actions/00_diplomatic_actions.txt`
- `0046-Apply-reward-from-fra_london-even-if-FRA-changes-tag.patch`: `common/great_projects/01_monuments.txt`
- `0053-Fix-temple-bonus-when-switching-between-reforms.patch`: `common/government_reforms/06_government_reforms_common.txt`
- `0077-Apply-absolutism-impact-from-court-ideas-to-all-privileges.patch`: `common/estate_privileges/02_noble_privileges.txt`, `common/estate_privileges/03_burgher_privileges.txt`
- `0089-make-asha-monarchy-work-for-custom-nations.patch`: `common/government_reforms/01_government_reforms_monarchies.txt`

## missing

- `0001-fix-Hanlin-Academy-modifier-for-korean-and-japanese-missions.patch`: `common/province_triggered_modifiers/00_modifiers.txt`
- `0002-prevent-event-728-Claims-on-Our-Rivals-from-firing-with-no-valid-province.patch`: `events/RandomEvents.txt`
- `0003-align-conditions-for-Fate-of-the-Mandate-with-its-tooltip.patch`: `missions/DOM_Chinese_Missions.txt`
- `0004-allow-mission-Fate-of-the-Mandatefate_of_the_mandate-to-be-completed-by-dismantling-the-mandate.patch`: `missions/DOM_Chinese_Missions.txt`
- `0005-partial-fix-for-hussite-incident-when-emperor-changes.patch`: `events/Incident_HussiteProtest.txt`
- `0007-Dont-remove-zoroastrian_prophet_in_the_court-when-firing-different-advisor.patch`: `common/scripted_effects/01_scripted_effects_for_on_actions.txt`
- `0008-fix-branching-missions-when-forming-a-country-while-having-branching-buttons.patch`: `common/scripted_effects/02_scripted_effects_preview_missions.txt`
- `0009-increase-manpower-from-boh_reformatio_sigismundi_hre.patch`: `common/event_modifiers/01_mission_modifiers.txt`
- `0011-re-enable-GC-missions-for-VAL-and-CAT-if-DOM-is-active.patch`: `missions/GC_Aragonese_Missions.txt`
- `0012-turn-MLO-into-a-monarchy-when-FRA-forms-a-PU-over-them.patch`: `events/FlavorFRA.txt`
- `0014-Fix-highlighting-for-Iroquois-missions.patch`: `missions/Iroquoians_Missions.txt`
- `0015-Allow-150-dev-free-company-for-SWE-Engelbrekt-mission.patch`: `missions/SCA_Swedish_Missions.txt`
- `0016-prevent-shwedagon_pagoda-from-getting-destroyed-by-countries-which-dont-own-it.patch`: `events/ChineseFactions.txt`
- `0017-prevent-Rotten-Borough-from-assigning-seat-to-territory.patch`: `events/Parlaments.txt`
- `0018-Only-allow-fifth-monarchists-reform-for-christian-custom-nations.patch`: `common/government_reforms/03_government_reforms_theocracies.txt`
- `0019-fix-expand-infrastructure-effect-for-Expand-the-Bogue-missions.patch`: `missions/DOM_Chinese_Missions.txt`, `missions/DOM_Japanese_Missions.txt`, `missions/Korean_Missions.txt`, `missions/zzzz_WoC_EoC_Yuan_Missions.txt`
- `0020-fix-or-remove-outdated-dynamic-names-for-the-province-Dortmund69.patch`: `common/province_names/aragonese.txt`, `common/province_names/castillian.txt`, `common/province_names/czech.txt`, `common/province_names/czech_new.txt`, `common/province_names/french.txt`, `common/province_names/irish.txt` (+5)
- `0021-Allow-son_modernize_army-to-be-completed-without-CoC.patch`: `missions/AFR_Songhai_Missions.txt`
- `0022-fix-tooltip-son_own_develop_clothes_and_salt_ct.patch`: `localisation/origins_l_english.yml`
- `0023-Fix-encoding-in-the-tutorial.patch`: `tutorial/eu4_tutorial_chapter1.eu4`, `tutorial/eu4_tutorial_chapter10.eu4`, `tutorial/eu4_tutorial_chapter2.eu4`, `tutorial/eu4_tutorial_chapter3.eu4`, `tutorial/eu4_tutorial_chapter4.eu4`, `tutorial/eu4_tutorial_chapter5.eu4` (+2)
- `0024-Fix-construction-of-Suez-canal-with-inflation-in-event-flavor_mam115.patch`: `events/flavorMAM.txt`
- `0026-let-LAE-keep-BYZ-missions-if-they-were-created-by-HAB.patch`: `missions/WoC_Austrian_Missions.txt`
- `0027-fix-highlighting-in-mission-Korean-Self-Reliance-kor_achieve_juche.patch`: `missions/Korean_Missions.txt`
- `0029-fix-patriarch-authority-in-swedish-eventsdecision.patch`: `decisions/SwedishDecisions.txt`, `events/FlavorSWE.txt`
- `0030-avoid-permaclaims-on-sea-tiles-from-GER-and-JAP-missions.patch`: `missions/DOM_Japanese_Missions.txt`, `missions/WOC_German_Missions.txt`
- `0031-remove-extra-spaces-before-regal-numbers.patch`: `common/countries/Aden.txt`, `common/countries/Alodia.txt`, `common/countries/Anizah.txt`, `common/countries/Antemoro.txt`, `common/countries/Austria.txt`, `common/countries/Austriahungary.txt` (+101)
- `0033-Fix-reconquest-war-against-Kalmyks-if-the-owner-doesnt-have-full-cores.patch`: `events/flavorKLM.txt`
- `0034-Fix-burgundian-inheritance-for-non-monarchies.patch`: `events/Incident_Burgundian_Inheritance.txt`
- `0035-fix-Seljuk-Empire-name-when-forming-Rum-as-Aq-and-Qara-Qoyunlu.patch`: `decisions/TurkishNation.txt`
- `0036-update-event-insight-for-flavor_ARB5-in-YEM_zaidi_caliphate.patch`: `missions/KoK_Yemen_Missions.txt`
- `0037-fix-portrait-of-female-Indian-master-recruiter.patch`: `dlc/dlc093_dharma_advisors/interface/countryview_dharma.gfx`
- `0038-use-mesoamerican-advisor-portraits-for-new-cultures.patch`: `dlc/dlc033_el_dorado/interface/countryview_mesoamerica.gfx`
- `0039-prevent-incan-event-Policies-of-Huascar-after-the-end-of-the-civil-war.patch`: `events/flavorINC.txt`
- `0040-Prevent-burghers-agenda-Expand-our-Colony-in-xestate_burghers_colonial_nation-for-countries-which-cant-spawn-CNs.patch`: `common/estate_agendas/03_burgher_agendas.txt`
- `0041-Prevent-eunuchs-agenda-Reform-the-Government-if-the-examination-system-reform-is-not-available.patch`: `common/estate_agendas/09_eunuchs_agendas.txt`
- `0042-Align-requirements-of-Eagle-of-Lbeck-mission-with-tooltip-and-add-fallback-if-there-are-no-valid-rivals.patch`: `missions/99_Hansa_Missions.txt`
- `0043-give-japan-claims-on-korea-if-DOM-is-active.patch`: `decisions/JapaneseNation.txt`
- `0044-Do-not-remove-estuarygranary-modifiers-from-flavor_mam102-if-the-provinces-get-conquered.patch`: `events/flavorMAM.txt`
- `0045-Allow-anglican-and-AVE-to-trigger-event-Huguenot-Rebels-Need-Our-Helptyw_events12.patch`: `events/TYWEvents.txt`
- `0047-Require-fur-province-in-the-new-world-for-Natives-Not-Assisting.patch`: `events/RandomEvents.txt`
- `0048-Make-Persian-mission-Checks-and-Balance-work-with-all-estates.patch`: `missions/KoK_Persia_Missions.txt`
- `0050-fix-Portuguese-missions-in-RNW-games.patch`: `missions/GC_Portuguese_Missions.txt`
- `0051-Fix-wrong-HRE-membership-after-looking-at-other-start-dates.patch`: `history/provinces/101 - Genoa.txt`, `history/provinces/102 - Nice.txt`, `history/provinces/103 - Piedmont.txt`, `history/provinces/104 - Milan.txt`, `history/provinces/105 - Parma.txt`, `history/provinces/107 - Brescia.txt` (+24)
- `0052-Fix-highlight-for-prussian_nation_general-decision.patch`: `decisions/PrussianNation.txt`
- `0054-add-scrollbar-to-naval-doctrines-if-there-are-more-than-5.patch`: `interface/countrymilitaryview.gui`
- `0055-Make-it-more-likely-that-an-emperor-who-has-a-negative-opinion-of-Burgundy-bans-their-entry-in-the-incident-Burgundy-and-the-Empire.patch`: `events/Incident_Burgundy_Joins_Empire.txt`
- `0056-Do-not-remove-Expanded-Daugava-Estuary-modifier-from-Riga-if-province-changes-hands.patch`: `missions/SCA_Polish_Missions.txt`
- `0057-Also-allow-Expanded-Daugava-Estuary-modifier-in-all-triggers-which-check-for-the-normal-modifier.patch`: `common/scripted_triggers/01_scripted_triggers_province_modifiers.txt`, `events/SiberianColonization.txt`
- `0059-Make-sure-that-A-Pretender-arises-always-has-an-event-option.patch`: `events/Purple_Phoenix_events.txt`
- `0060-fix-highlighting-in-Ottoman-base-game-mission-Conquer-Greececonquer_southern_greece.patch`: `missions/Ottoman_Missions.txt`
- `0061-fix-highlighting-in-City-of-the-Worlds-Desiredefeat_the_byzantine_empire.patch`: `missions/Ottoman_Missions.txt`
- `0062-Fix-highlighting-in-St-Olav-Towerfin_neva.patch`: `missions/SCA_Finnish_Missions.txt`
- `0063-Fix-reward-when-completing-Defense-in-DepthBYZ_defence_in_depth-with-level-3-Theodosian-Walls.patch`: `missions/KoK_Byzantine_Missions.txt`
- `0064-Make-reform-Ganden-Phodrang-available-to-Sino-Tibetan-countries.patch`: `common/government_reforms/03_government_reforms_theocracies.txt`
- `0065-Fix-devastation-trigger-and-highlighting-for-Fortify-the-Coast-missions.patch`: `missions/DOM_Chinese_Missions.txt`, `missions/DOM_Japanese_Missions.txt`, `missions/Korean_Missions.txt`
- `0066-Bring-tooltips-of-Fortify-the-Coast-missions-more-in-line-with-the-effects.patch`: `missions/DOM_Chinese_Missions.txt`, `missions/DOM_Japanese_Missions.txt`, `missions/Korean_Missions.txt`
- `0067-Cede-goa-to-the-correct-nation-in-the-event-Vasco-da-Gama-in-India.patch`: `events/FlavorPOR.txt`
- `0068-Allow-Portuguese-missions-to-be-completed-after-forming-another-country.patch`: `missions/GC_Portuguese_Missions.txt`, `missions/Portuguese_Missions.txt`
- `0069-Reduce-amount-of-land-gain-for-successful-eunuch-rebels-from-100-to-10.patch`: `common/rebel_types/eunuch_rebels.txt`
- `0071-Prevent-Hawaii-and-Viti-formation-in-random-nation-games.patch`: `decisions/FijiNation.txt`, `decisions/HawaiiNation.txt`
- `0072-Make-Constitutional-Restoration-event-give-alternative-reforms-for-countries-which-cant-have-the-Parliamentarism-reform.patch`: `events/Governments.txt`
- `0073-Prevent-event-A-Zoroastrian-Identity-during-war.patch`: `events/FlavorPER.txt`
- `0074-Custom-militarization-idea-now-also-gives-earlylate-militarization.patch`: `common/custom_ideas/02_newer_ideas.txt`
- `0075-Give-countries-with-Margravate-reform-another-reform-if-Domination-isnt-active.patch`: `history/countries/BAD - Baden.txt`, `history/countries/BRA - Brandenburg.txt`, `history/countries/MFA - Montferrat.txt`
- `0076-Prevent-high-base-unrest-from-janissary-disaster.patch`: `decisions/Ottoman.txt`, `events/disaster_ottoman_power_struggle.txt`
- `0077-Apply-absolutism-impact-from-court-ideas-to-all-privileges.patch`: `common/estate_privileges/08_janissaries_privileges.txt`, `common/estate_privileges/10_qizilbash_privileges.txt`, `common/estate_privileges/11_ghulams_privileges.txt`
- `0078-Add-missing-perma-claims-on-muslim-provinces-to-arabia-mission-event-Second-Islamic-Golden-Age.patch`: `common/scripted_effects/03_scripted_effects_for_mission_rewards.txt`
- `0079-Fix-United-Horn-modifier-from-horn-of-africa-missions.patch`: `common/event_modifiers/01_mission_modifiers.txt`
- `0080-Fix-highlighting-for-Restore-the-Mongol-Empire.patch`: `decisions/MongolEmpire.txt`
- `0082-Fix-renaming-to-Lithuanian-Polish-Commonwealth-when-forming-PLC-as-LIT.patch`: `decisions/TheCommonwealth.txt`
- `0083-Fix-renaming-to-The-Hanseatic-League-when-forming-HSA.patch`: `decisions/HanseaticLeague.txt`
- `0084-Fix-maritime-idea-reward-from-venetian-mission-Masters-of-the-Sea.patch`: `missions/WOC_Venetian_Missions.txt`
- `0086-Fix-second-reward-for-Yuan-mission-Reform-Civil-Registration.patch`: `common/scripted_triggers/02_scripted_triggers_for_mission_conditions.txt`
- `0087-make-new-ruler-traits-available-to-custom-nations.patch`: `common/ruler_personalities/00_core.txt`
- `0090-reduce-duration-of-CBs-which-last-for-more-than-100-years.patch`: `events/flavorBNG.txt`, `events/flavorETH.txt`, `events/flavorJNP.txt`, `events/flavorNOL.txt`
- `0091-make-the-Kalpi-war-event-chain-about-Kalpi-instead-of-Bundelkhand.patch`: `events/flavorJNP.txt`
- `0092-bring-tooltip-in-flavor_eth13-in-line-with-effect-in-flavor_eth11.patch`: `events/flavorETH.txt`
- `0093-fix-removing-of-prestige-penalty-when-changing-secondary-religion-after-completing-For-the-Horde.patch`: `customizable_localization/00_customizable_localization_FR.txt`, `missions/zzz_WoC_Shared_Horde_Missions.txt`
- `0094-Pay-out-rewards-for-correct-nodes-in-venitian-mission-Carve-New-Routesven_triangle_trade.patch`: `missions/WOC_Venetian_Missions.txt`
- `0095-Allow-Mongol-Empire-formed-by-Yuan-to-keep-Yuan-missions-when-switching-branches.patch`: `missions/WoC_Mongolian_Missions.txt`
- `0096-Prevent-error-messages-when-the-HRE-is-dismantled.patch`: `common/scripted_functions/00_scripted_functions.txt`
- `0097-Make-sure-that-BYZ-has-correct-missions-when-released-from-the-PLC-mission-Purple-Phoenix.patch`: `events/flavorPOL.txt`
- `0098-Disable-Ghilman-Rebels-for-countries-without-the-estate.patch`: `common/rebel_types/ghulams_rebels.txt`
- `0099-Disable-Qizilbash-Rebels-for-countries-without-the-estate.patch`: `common/rebel_types/qizilbash_rebels.txt`
- `0100-prevent-native_federations_event2-from-happening-over-and-over-again.patch`: `events/Native_Federation_Events.txt`
- `0101-Make-Cernida-Fortifications-bonus-available-for-higher-level-forts.patch`: `common/buildings/00_buildings.txt`
- `0102-Fix-separatism-reward-in-oceania_unite_home_region.patch`: `missions/Oceania_Missions.txt`
- `0103-Allow-completing-Drua-Buildersfiji_drua_builders-also-with-grand-shipyards.patch`: `missions/Polynesian_TAGs_Missions.txt`
- `0104-Prevent-HSA-from-switching-to-generic-ideas-in-flavor_hsa26.patch`: `events/flavorHSA.txt`
- `0105-prevent-pomeranian-ideas-from-overriding-tag-specific-ideas.patch`: `common/ideas/zz_group_ideas.txt`
- `0106-Give-florentine-missions-when-forming-Tuscany.patch`: `decisions/TuscanNation.txt`
- `0108-prevent-building-temple-in-colonial_nation191-if-the-province-already-has-a-cathedral.patch`: `events/ColonialNation.txt`
- `0109-prevent-building-temples-if-there-is-already-a-cathedral.patch`: `events/Inti.txt`, `events/OrderEvents.txt`, `events/SikhEvents.txt`, `events/Totemism.txt`, `events/flavorAIMARA.txt`, `events/flavorETH.txt` (+2)
- `0110-release-VOC-with-idea-groups-filled-and-correct-national-ideas.patch`: `decisions/VOC_decisions.txt`
- `0111-Restrict-trigger-of-flavor_brapru1-to-prevent-unintenional-situations.patch`: `events/flavorBRAPRU.txt`
- `0112-try-to-fix-Napoleons-dynasty-in-a-republic.patch`: `events/disaster_french_revolution.txt`
- `0113-Dont-upgrade-MAM_ideas-if-the-country-has-other-ideas.patch`: `missions/KoK_Mamluks_Missions.txt`
- `0114-prevent-Raze-our-Enemies-if-you-cant-raze.patch`: `common/estate_agendas/05_nomadic_tribe_agendas.txt`
- `0115-Dont-show-new-missions-when-forming-Rum-if-you-dont-get-new-missions.patch`: `decisions/TurkishNation.txt`
- `0116-remove-generic-reform_religion-mission-for-players-without-the-DLCs.patch`: `missions/New_World_Missions.txt`
- `0117-remove-modifier-geo_rus_alliance-when-alliance-is-broken.patch`: `common/scripted_effects/01_scripted_effects_for_on_actions.txt`
- `0118-Unlock-the-republic-and-monarchy-reforms-when-proclaiming-emperor-as.patch`: `common/government_reforms/02_government_reforms_republics.txt`, `events/FlavorRUS.txt`
- `0119-fix-modifier-duration-in-tooltips-of-jap_japanese_economic_miracle.patch`: `missions/DOM_Japanese_Missions.txt`
- `0120-fix-goods-produced-modifiers-from-event-flavor_aju1.patch`: `common/event_modifiers/01_mission_modifiers.txt`
- `0121-Also-allow-upgraded-buildings-in-all-missions-which-require-a-building.patch`: `missions/99_Hansa_Missions.txt`, `missions/Cherokee_Missions.txt`, `missions/DH_Bahmani_Missions.txt`, `missions/GC_Granadan_Missions.txt`, `missions/GC_Moroccan_Missions.txt`, `missions/GC_Tunis_Missions.txt` (+2)
- `0122-make-mission-rewards-for-forts-available-for-all-fort-buildings.patch`: `common/buildings/00_buildings.txt`
- `0123-Allow-mission-Stones-of-Ganesh-be-completed-without-Brahmins-estate.patch`: `missions/MND_Tondo_Missions.txt`
- `0124-Add-fallbacks-for-missions-which-require-clergy-loyalty.patch`: `missions/Oceania_Missions.txt`, `missions/SCA_Danish_Missions.txt`, `missions/SCA_Lithuania_Missions.txt`
- `0125-Add-fallbacks-for-missions-which-require-clergy-influence.patch`: `missions/DH_Bahmani_Missions.txt`, `missions/DH_Taungu_Missions.txt`
- `0126-Prevent-volcanic-eruption-from-happening-for-the-same-province-twice.patch`: `events/Volcano_events.txt`
