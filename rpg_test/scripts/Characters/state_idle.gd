class_name State_Idle extends State

## Stores a reference to the player that this state belongs to

@onready var walk : State = $"../Walk"
@onready var attack : State = $"../Attack"

## What happens when the player enters this State?
func Enter() -> void:
	player.UpdateAnimation("idle")
	pass

## What happens when the player exits this State?
func Exit() -> void:
	pass

## What happens during the process update in this State?
func Process(_delta : float) -> State:
	player.velocity = Vector2.ZERO
	if player.direction != Vector2.ZERO:
		return walk
	return null

## What happens during the physics process update in this State?
func Physics (_delta : float) -> State:
	return null

## What happens when an input event is received in this State?
func HandleInput(_event : InputEvent) -> State:
	if _event.is_action_pressed("attack"):
		return attack
	return null
