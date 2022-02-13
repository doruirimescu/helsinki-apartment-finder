# decision-making

# A software framework to enable decision making

* Based on socratic model
* Simple user interface that guides the user by asking questions
* Two parts: model building and data building

## Model
* The model describes the setup for the decision making problem
* The model can be open-loop (once a decision is made, it cannot be repeated, eg. buying an apartment)
* The model can be closed-loop (decisions can be repeated
* The model is created by the user
* Model can be based on SWOT
* Each model parameter is normalized from 0 to 100
* Each model parameter can be numeric or textual
* The user is guided to create a normalized parameter
* All parameters are expressed in terms of rewards
* All parameters can be distributed on a circle with radius of 100
* Parameters can be normalized automatically by relative comparison. Or absolute comparison can be made by user
* For each parameter, user specifies if higher value is better
*

### Closed-loop model
* Optimizable via Kalman-filter approach

### Open-loop model
* Can it be transformed into a closed-loop model ? That means, finding data about similar decisions taken by others in the past
* Can generate a poll if convertible to closed-loop model

## Data
* For a chosen (created) model, data is entered
* Radar chart is created

## Example
* Open-loop model: Buying an apartment
* Closed-loop model: deciding each day how many hours to watch tv, how many hours to exercise, etc

# Buying an apartment
## Model
### Parameters
Parameters are normalized by relating each data entry. Ex after entering data for 5 apartments, min and max are converted from 0 to 100. All the others come in between.

* Price
* Area sqm
* Year of construction
* Vastike
* Floor
* Zone
* Distance to closest mall
* (Distance to school)
* (Distance to recreational areas)
