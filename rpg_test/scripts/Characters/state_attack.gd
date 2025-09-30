class_name State_Attack extends State

var attacking : bool = false
## Stores a reference to the player that this state belongs to

@export var attack_sound : AudioStream
@export_range(1, 20, 0.5) var decelerate_speed : float = 5.0

@onready var walk : State = $"../Walk"
@onready var attack : State = $"../Attack"
@onready var idle : State = $"../Idle"
@onready var animation_player : AnimationPlayer = $"../../AnimationPlayer"
@onready var attack_anim : AnimationPlayer = $"../../Sprite2D/AttackEffectSprite/AnimationPlayer"
@onready var audio : AudioStreamPlayer2D =$"../../Audio/AudioStreamPlayer2D"


## What happens when the player enters this State?
func Enter() -> void:
	player.UpdateAnimation("attack")
	attack_anim.play("attack_"+ player.AnimDirection())
	animation_player.animation_finished.connect(EndAttack)

	audio.stream = attack_sound
	audio.pitch_scale = randf_range(0.9, 1.1)
	audio.play()
	attacking = true
	pass

## What happens when the player exits this State?
func Exit() -> void:
	animation_player.animation_finished.disconnect(EndAttack)
	attacking = false
	pass

## What happens during the process update in this State?
func Process(_delta : float) -> State:
	player.velocity -= player.velocity * decelerate_speed * _delta
	if attacking == false:
		if player.direction == Vector2.ZERO:
			return idle
		else:
			return walk
	return null

## What happens during the physics process update in this State?
func Physics (_delta : float) -> State:
	return null

## What happens when an input event is received in this State?
func HandleInput(_event : InputEvent) -> State:
	return null

func EndAttack(_newAnimName : String) -> void:
	attacking = false
