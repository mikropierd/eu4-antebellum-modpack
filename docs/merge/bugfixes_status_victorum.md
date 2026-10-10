# Bugfixes -> Victorum: status

Wynik nakładania patchy z grotaclasBugfixes (per plik, wszystko-albo-nic).

| status | liczba |
|---|---|
| applied | 214 |
| already | 2 |
| missing | 45 |
| conflict | 64 |

- applied: nałożone
- already: poprawka już jest w pliku
- missing: pliku nie ma w tym repo (dla Antebellum: jest w bazowym modzie Ante Bellum)
- conflict: plik jest, ale hunki nie pasują (wymaga ręcznego scalenia)


## conflict

- `0006-make-confucian-monuments-work-with-harmonized-religious-groups.patch`: `common/great_projects/01_monuments.txt`
- `0019-fix-expand-infrastructure-effect-for-Expand-the-Bogue-missions.patch`: `missions/DOM_Japanese_Missions.txt`
- `0020-fix-or-remove-outdated-dynamic-names-for-the-province-Dortmund69.patch`: `common/province_names/czech.txt`, `common/province_names/polish.txt`, `common/province_names/schlesian.txt`
- `0026-let-LAE-keep-BYZ-missions-if-they-were-created-by-HAB.patch`: `missions/WoC_Austrian_Missions.txt`
- `0028-allow-custom-nations-to-keep-livonian-reforms.patch`: `common/government_reforms/01_government_reforms_monarchies.txt`
- `0030-avoid-permaclaims-on-sea-tiles-from-GER-and-JAP-missions.patch`: `missions/DOM_Japanese_Missions.txt`
- `0031-remove-extra-spaces-before-regal-numbers.patch`: `common/countries/Alodia.txt`, `common/countries/Ayyubids.txt`, `common/countries/Carib.txt`, `common/countries/Charrua.txt`, `common/countries/Makuria.txt`, `common/countries/Nubia.txt`
- `0034-Fix-burgundian-inheritance-for-non-monarchies.patch`: `events/Incident_Burgundian_Inheritance.txt`
- `0035-fix-Seljuk-Empire-name-when-forming-Rum-as-Aq-and-Qara-Qoyunlu.patch`: `decisions/TurkishNation.txt`
- `0043-give-japan-claims-on-korea-if-DOM-is-active.patch`: `decisions/JapaneseNation.txt`
- `0046-Apply-reward-from-fra_london-even-if-FRA-changes-tag.patch`: `common/great_projects/01_monuments.txt`
- `0051-Fix-wrong-HRE-membership-after-looking-at-other-start-dates.patch`: `history/provinces/101 - Genoa.txt`, `history/provinces/102 - Nice.txt`, `history/provinces/103 - Piedmont.txt`, `history/provinces/104 - Milan.txt`, `history/provinces/105 - Parma.txt`, `history/provinces/107 - Brescia.txt` (+24)
- `0052-Fix-highlight-for-prussian_nation_general-decision.patch`: `decisions/PrussianNation.txt`
- `0053-Fix-temple-bonus-when-switching-between-reforms.patch`: `common/government_reforms/06_government_reforms_common.txt`
- `0065-Fix-devastation-trigger-and-highlighting-for-Fortify-the-Coast-missions.patch`: `missions/DOM_Japanese_Missions.txt`
- `0066-Bring-tooltips-of-Fortify-the-Coast-missions-more-in-line-with-the-effects.patch`: `missions/DOM_Japanese_Missions.txt`
- `0071-Prevent-Hawaii-and-Viti-formation-in-random-nation-games.patch`: `decisions/FijiNation.txt`
- `0076-Prevent-high-base-unrest-from-janissary-disaster.patch`: `events/disaster_ottoman_power_struggle.txt`
- `0080-Fix-highlighting-for-Restore-the-Mongol-Empire.patch`: `decisions/MongolEmpire.txt`
- `0082-Fix-renaming-to-Lithuanian-Polish-Commonwealth-when-forming-PLC-as-LIT.patch`: `decisions/TheCommonwealth.txt`
- `0084-Fix-maritime-idea-reward-from-venetian-mission-Masters-of-the-Sea.patch`: `missions/WOC_Venetian_Missions.txt`
- `0087-make-new-ruler-traits-available-to-custom-nations.patch`: `common/ruler_personalities/00_core.txt`
- `0106-Give-florentine-missions-when-forming-Tuscany.patch`: `decisions/TuscanNation.txt`
- `0114-prevent-Raze-our-Enemies-if-you-cant-raze.patch`: `common/estate_agendas/05_nomadic_tribe_agendas.txt`
- `0115-Dont-show-new-missions-when-forming-Rum-if-you-dont-get-new-missions.patch`: `decisions/TurkishNation.txt`
- `0119-fix-modifier-duration-in-tooltips-of-jap_japanese_economic_miracle.patch`: `missions/DOM_Japanese_Missions.txt`
- `0121-Also-allow-upgraded-buildings-in-all-missions-which-require-a-building.patch`: `missions/GC_Granadan_Missions.txt`
- `0122-make-mission-rewards-for-forts-available-for-all-fort-buildings.patch`: `common/buildings/00_buildings.txt`

## missing

- `0016-prevent-shwedagon_pagoda-from-getting-destroyed-by-countries-which-dont-own-it.patch`: `events/ChineseFactions.txt`
- `0020-fix-or-remove-outdated-dynamic-names-for-the-province-Dortmund69.patch`: `common/province_names/czech_new.txt`, `common/province_names/polish_new.txt`, `common/province_names/schlesian_new.txt`
- `0022-fix-tooltip-son_own_develop_clothes_and_salt_ct.patch`: `localisation/origins_l_english.yml`
- `0023-Fix-encoding-in-the-tutorial.patch`: `tutorial/eu4_tutorial_chapter1.eu4`, `tutorial/eu4_tutorial_chapter10.eu4`, `tutorial/eu4_tutorial_chapter2.eu4`, `tutorial/eu4_tutorial_chapter3.eu4`, `tutorial/eu4_tutorial_chapter4.eu4`, `tutorial/eu4_tutorial_chapter5.eu4` (+2)
- `0029-fix-patriarch-authority-in-swedish-eventsdecision.patch`: `decisions/SwedishDecisions.txt`
- `0031-remove-extra-spaces-before-regal-numbers.patch`: `common/countries/Austriahungary.txt`, `common/countries/Rum.txt`
- `0037-fix-portrait-of-female-Indian-master-recruiter.patch`: `dlc/dlc093_dharma_advisors/interface/countryview_dharma.gfx`
- `0038-use-mesoamerican-advisor-portraits-for-new-cultures.patch`: `dlc/dlc033_el_dorado/interface/countryview_mesoamerica.gfx`
- `0040-Prevent-burghers-agenda-Expand-our-Colony-in-xestate_burghers_colonial_nation-for-countries-which-cant-spawn-CNs.patch`: `common/estate_agendas/03_burgher_agendas.txt`
- `0041-Prevent-eunuchs-agenda-Reform-the-Government-if-the-examination-system-reform-is-not-available.patch`: `common/estate_agendas/09_eunuchs_agendas.txt`
- `0045-Allow-anglican-and-AVE-to-trigger-event-Huguenot-Rebels-Need-Our-Helptyw_events12.patch`: `events/TYWEvents.txt`
- `0054-add-scrollbar-to-naval-doctrines-if-there-are-more-than-5.patch`: `interface/countrymilitaryview.gui`
- `0055-Make-it-more-likely-that-an-emperor-who-has-a-negative-opinion-of-Burgundy-bans-their-entry-in-the-incident-Burgundy-and-the-Empire.patch`: `events/Incident_Burgundy_Joins_Empire.txt`
- `0057-Also-allow-Expanded-Daugava-Estuary-modifier-in-all-triggers-which-check-for-the-normal-modifier.patch`: `events/SiberianColonization.txt`
- `0059-Make-sure-that-A-Pretender-arises-always-has-an-event-option.patch`: `events/Purple_Phoenix_events.txt`
- `0069-Reduce-amount-of-land-gain-for-successful-eunuch-rebels-from-100-to-10.patch`: `common/rebel_types/eunuch_rebels.txt`
- `0071-Prevent-Hawaii-and-Viti-formation-in-random-nation-games.patch`: `decisions/HawaiiNation.txt`
- `0077-Apply-absolutism-impact-from-court-ideas-to-all-privileges.patch`: `common/estate_privileges/08_janissaries_privileges.txt`
- `0083-Fix-renaming-to-The-Hanseatic-League-when-forming-HSA.patch`: `decisions/HanseaticLeague.txt`
- `0090-reduce-duration-of-CBs-which-last-for-more-than-100-years.patch`: `events/flavorJNP.txt`, `events/flavorNOL.txt`
- `0091-make-the-Kalpi-war-event-chain-about-Kalpi-instead-of-Bundelkhand.patch`: `events/flavorJNP.txt`
- `0098-Disable-Ghilman-Rebels-for-countries-without-the-estate.patch`: `common/rebel_types/ghulams_rebels.txt`
- `0099-Disable-Qizilbash-Rebels-for-countries-without-the-estate.patch`: `common/rebel_types/qizilbash_rebels.txt`
- `0100-prevent-native_federations_event2-from-happening-over-and-over-again.patch`: `events/Native_Federation_Events.txt`
- `0102-Fix-separatism-reward-in-oceania_unite_home_region.patch`: `missions/Oceania_Missions.txt`
- `0104-Prevent-HSA-from-switching-to-generic-ideas-in-flavor_hsa26.patch`: `events/flavorHSA.txt`
- `0109-prevent-building-temples-if-there-is-already-a-cathedral.patch`: `events/Inti.txt`, `events/OrderEvents.txt`, `events/Totemism.txt`, `events/flavorAIMARA.txt`
- `0110-release-VOC-with-idea-groups-filled-and-correct-national-ideas.patch`: `decisions/VOC_decisions.txt`
- `0116-remove-generic-reform_religion-mission-for-players-without-the-DLCs.patch`: `missions/New_World_Missions.txt`
- `0124-Add-fallbacks-for-missions-which-require-clergy-loyalty.patch`: `missions/Oceania_Missions.txt`
- `0126-Prevent-volcanic-eruption-from-happening-for-the-same-province-twice.patch`: `events/Volcano_events.txt`
