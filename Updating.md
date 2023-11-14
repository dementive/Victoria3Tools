# How To Update to new Vic3 Version

1. Run parse_docs.py and follow it's instructions

2. Add the generated data to the bottom of the auto-generated-content section in VictoriaScript.fake-sublime-syntax

3. Go to PluginData.py and run the get_game_data function.

4. With the printed output, replace the proper lists in PluginData.py


# Bugs

• goto definition popups wrongly show the definition of something as a reference if it is defined in the same file as the current token

• reload plugin command broke?

## Todo

• Fix shader syntax so it correctly shows `//` comments when on Code[[ ]] blocks and `#` commments when not in Code blocks

• Add phantom popups that show color of named colors with the "entity.name.named.colors" scope assigned to them

• Add a new hover popup for usages of @words preprocessor statements. When hovering over the usages it will show a simple popup that shows what the value of the statement is. Should work for gui and script.

• Add ⨉ character to top corner of texture phantom popups to close them

• Write parser for Data system functions in data types log.

• Special autocompletion triggers for event, decision, and journal files

• Custom parsers for different GameObjects that save more useful information that can be used in popups

# Autocomplete Objects and their associations in game

### Proposal types

post_proposal

### Discrimination traits

has_discrimination_trait

### Countries

c:


### Country Ranks

rank_value:


### Ai Strats

has_strategy = x
set_strategy = x

### Buildings

start_building_construction
remove_building
start_building_construction
activate_building
deactivate_building
start_privately_funded_building_construction
building
building_type
has_building
is_building_type
pop_employment_building
has_active_building
set_available_for_autonomous_investment

### Battle Conditions

has_battle_condition

### Building Group

force_resource_depletion
force_resource_discovery
pop_employment_building_group
is_building_group
has_potential_resource

remaining_undepleted = {
	type = bg_rubber
	amount > 1
}

## Character Traits

add_trait
remove_trait
has_trait

create_character = {
	traits = {
		imperious
		expensive_tastes
	}
}

### Cultures

scope - cu:

has_culture_graphics
country_has_primary_culture
has_pop_culture
is_homeland
add_homeland
remove_homeland
culture


### Decrees

scope - decree_cost:
has_decree

### Diplomatic Actions

is_diplomatic_action_type

can_afford_diplomatic_action = {
    type = <diplomatic_action>
}
has_diplomatic_pact = {
    type = <diplomatic_action>
}
create_diplomatic_pact = {
    type = <diplomatic_action>
}
remove_diplomatic_pact = {
    type = <diplomatic_action>
}

### Diplomatic Plays

is_diplomatic_play_type

create_diplomatic_play = {
    type = <diplomatic_play>
}

### Game Rules

has_game_rule

### Trade Goods
scopes - goods:, g:
add_cultural_obsession
remove_cultural_obsession
is_taxing_goods
has_cultural_obsession
is_banning_goods

alias[effect:create_trade_route] = {
    goods = <goods>
}

taboos = {
    good1
    good2
}

### Gov Types

has_government_type

### Ideologies

has_ideology
set_ideology
add_ideology
remove_ideology
ideology

ideologies = {
    ideology1
    ideology2
}

### Institutions

scope - institution:
expanding_institution
has_institution
institution

### Interest Group Traits

### Interest Groups

scopes - ig:, interest_group:
has_ruling_interest_group
is_interest_group_type
law_approved_by
interest_group

set_ruling_interest_groups = {
	ig_landowners
}

### Journal Entries

scope - je:
has_journal_entry

add_journal_entry = {
    type = <journal_entry>
}

### Law Groups

scope - active_law:

### Laws

scope - law_type:

all of the effects/triggers for law_type use the scope

unlocking_laws = {
    law1
    law2
}

possible_political_movements = {
    law1
    law2
}

### Modifiers

has_modifier
remove_modifier

add_modifier = {
    name = <modifier>
    duration = int
    multiplier = value
    is_decaying = bool
}
add_enactment_modifier = {
    name = <modifier>
}

### Parties

scopes - py:, party:
is_party_type

### Pop Needs

No effects/triggers/scopes

### Pop Types

scope - pop_type:
is_pop_type
pop_type

### Production Method Groups

No effects/triggers/scopes

### Production Methods


has_active_production_method
production_method

### Religions

scopes - rel:, religion:

has_pop_religion
religion

### State Traits

has_state_trait

### Strategic Regions

scope - sr:

add_declared_interest
has_interest_marker_in_region
hq

### Subject Types

is_subject_type
change_subject_type

can_have_as_subject = {
    type = <subject_type>
}

### Technologies

add_technology_researched
can_research
has_technology_progress
has_technology_researched
is_researching_technology
is_researching_technology_category
technology

unlocking_technologies = {
    tech1
    tech2
}

### Terrains

has_terrain

### State Regions

scopes - s:

set_capital
set_market_capital
country_or_subject_owns_entire_state_region
has_state_in_state_region
owns_entire_state_region
owns_treaty_port_in



### Boolean Effects

set_subsidized
free_character_from_void
kill_character
hidden
remove_as_interest_group_leader
set_as_interest_group_leader
abandon_revolution
add_ruling_interest_group
join_revolution
remove_ruling_interest_group
set_ig_bolstering
set_ig_suppression
set_ruling_party
subsidized
deactivate_parties
start_research_random_technology
update_party_support
primary_demand

### Boolean Triggers

is_revolutionary
market_has_goods_shortage
has_high_attrition
is_attacker_in_battle
is_busy
is_character_alive
is_defender_in_battle
is_female
is_heir
is_in_battle
is_in_void
is_mobilized
is_monarch
is_on_front
is_repairing
is_ruler
is_traveling
is_trade_route_active
is_trade_route_productive
trade_route_needs_convoys_to_grow
has_diplomatic_play
always
has_game_started
has_reached_end_date
is_game_paused
is_gamestate_tutorial_active
is_objective_completed
is_tutorial_active
should_show_nudity
is_province_land
is_interest_active
aggressive_diplomatic_plays_permitted
approaching_bureaucracy_shortage
can_have_subjects
enacting_any_law
has_active_peace_deal
has_any_secessionists_broken_out
has_any_secessionists_growing
has_any_secessionists_possible
has_convoys_being_sunk
has_decreasing_interests
is_initiator
has_free_government_reform
has_global_highest_gdp
has_global_highest_innovation
has_healthy_economy
has_insurrectionary_interest_groups
has_possible_decisions
has_researchable_technology
has_revolution
has_sufficient_construction_capacity_for_investment
has_wasted_construction
in_default
in_election_campaign
is_ai
is_at_war
is_construction_paused
is_country_alive
is_diplomatic_play_committed_participant
is_diplomatic_play_initiator
is_diplomatic_play_target
is_diplomatic_play_undecided_participant
is_expanding_institution
is_in_customs_union
is_junior_in_customs_union
is_local_player
is_losing_power_rank
is_player
is_secessionist
is_subject
leads_customs_union
should_set_wargoal
taking_loans
culture_accepted
has_ongoing_assimilation
has_ongoing_conversion
has_state_religion
is_employed
pop_has_primary_culture
pop_is_discriminated
religion_accepted
building_has_goods_shortage
has_failed_hires
is_buildable
is_government_funded
is_subsidized
is_subsistence_building
is_under_construction
is_tradeable
is_diplomatic_pact_in_danger
has_port
has_party
is_being_bolstered
is_being_suppressed
is_in_government
is_insurrectionary
is_marginal
is_powerful
is_land_theater
has_assimilating_pops
has_converting_pops
is_capital
is_coastal
is_in_revolt
is_incorporated
is_isolated_from_market
is_largest_state_in_region
is_mass_migration_target
is_sea_adjacent
is_slave_state
is_split_state
is_treaty_port
is_under_colonization
state_has_goods_shortage
is_consumed_by_government_buildings
is_consumed_by_military_buildings
market_goods_has_goods_shortage
is_state_region_land
is_goal_complete
is_progressing
is_war