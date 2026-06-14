import asyncio
import json

import tkinter as tk
import tkinter.messagebox as mb
from tkinter import Frame, ttk, Tk

from game import game_manager
from game.classes.items import *
from config import RESOURCES_DIR, init_db

async def save(manager, object):
    await init_db()
    await manager.add(object)


class ResourceCreator:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Resource Creator")
        self.root.configure(background="#2e2e2e")
        self.root.geometry("1800x1000+20+20")
        self.resource_type = None

    def get_items_identificators_from_db(self) -> list[str]:
        
        return []

    def show_error(self, message: str):
        mb.showerror(title="Ошибка!", message=message)

    def show_info(self, message: str):
        mb.showinfo(title="Информация", message=message)

    def show_warn(self, message: str):
        mb.showwarning(title="Внимание!", message=message)

    def start(self):
        self.clear_all_inside_frame(self.root)
        tk.Label(self.root, text="Resource Creator", font=("Arial", 24), bg="#2e2e2e", fg="#ffffff").pack(pady=20)
        tk.Label(self.root, text="This is a tool for creating game resources such as enemies, items, and locations.", font=("Arial", 14), bg="#2e2e2e", fg="#ffffff").pack(pady=10)
        tk.Label(self.root, text="Select a resource type to create:", font=("Arial", 14), bg="#2e2e2e", fg="#ffffff").pack(pady=10, padx=10)
        tk.Button(self.root, text="Items", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=self.create_item).pack(pady=5)
        tk.Button(self.root, text="Entities", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=self.create_entity).pack(pady=5)
        tk.Button(self.root, text="Quests", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=self.create_quest).pack(pady=5)
        tk.Button(self.root, text="Обзор ресурсов", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=self.show_resources).pack(pady=5)

        self.root.mainloop()

    def create_item(self):
        def save_item():
            item_name = name_entry.get()
            item_type = item_type_combobox.get()
            item_rarity = rarity_combobox.get()
            item_stackable = stackable_var.get()
            item_description = description_text.get("1.0", "end-1c")
            item_identificator = identificator_entry.get()
            item_value = value_var.get()
            if not all([item_name, item_type, item_rarity, item_description, item_identificator]):
                self.show_warn("Одно из обязательных полей не заполнено!")
                return
            item_dict = {
                "identificator": item_identificator.lower(),
                "type": item_type.lower(),
                "name": item_name.capitalize(),
                "rarity": item_rarity.lower(),
                "stacked": item_stackable,
                "value": item_value,
                "description": item_description
            }
            item = None
            if self.resource_type == "Weapon":  
                item = Weapon(data=item_dict)
                
                item.slot = slot_combobox.get().lower()
                physical_damage = physical_damage_var.get()
                cold_damage = cold_damage_var.get()
                fire_damage = fire_damage_var.get()
                lightning_damage = lightning_damage_var.get()
                attack_speed = attack_speed_var.get()
                crit_chance = crit_chance_var.get()
                crit_multiplier = crit_multiplier_var.get()

                item_damage = item.stats.damage
                item_damage.physical.value = physical_damage
                item_damage.fire.value = fire_damage
                item_damage.cold.value = cold_damage
                item_damage.lightning.value = lightning_damage
                item.stats.attack_speed = attack_speed
                item.stats.crit = crit_chance
                item.stats.crit_multy = crit_multiplier
                item.durability.max_durability = durability_var.get()
                item.durability.repair()
                item.equip_requirements.level = level_requirement_var.get()
                item.equip_requirements.strength = strength_requirement_var.get()
                item.equip_requirements.agility = agility_requirement_var.get()
                item.equip_requirements.intelligence = intelligence_requirement_var.get()

            elif self.resource_type == "Armor":
                ...
            elif self.resource_type == "Jewelry":
                ...
            elif self.resource_type == "Utility":
                ...
            elif self.resource_type == "Consumable":
                ...
            elif self.resource_type == "Materials":
                item = Material(data=item_dict)
            else:
                return
            asyncio.run(save(game_manager.item_manager, item))
            self.show_info("Предмет успешно сохранен в базу данных.")

        def create_item_fields(item_type, resource_frame: Frame):
            self.clear_all_inside_frame(resource_frame)
            if not item_type:
                return
            if resource_frame.winfo_children():
                return
            self.resource_type = item_type
            if item_type == "Weapon":
                global physical_damage_var, fire_damage_var, cold_damage_var, lightning_damage_var, attack_speed_var, crit_chance_var, crit_multiplier_var, attribute_scale_bool_var, attribute_combobox, attribute_scale_power_var, slot_combobox
                global level_requirement_var, strength_requirement_var, agility_requirement_var, intelligence_requirement_var, durability_var
                damage_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                damage_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(damage_frame, text="Damage:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)

                physical_damage_frame = tk.Frame(damage_frame, bg="#383838", width=200, height=50)
                physical_damage_frame.pack(side=tk.LEFT, anchor="w")
                physical_damage_var = tk.DoubleVar()
                tk.Label(physical_damage_frame, text="Physical:", font=("Arial", 14), bg="#727272", fg="#ffffff").pack(side=tk.LEFT)
                physical_damage_spinbox = tk.Spinbox(physical_damage_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=physical_damage_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                physical_damage_spinbox.pack(side=tk.RIGHT, padx=5)

                fire_damage_frame = tk.Frame(damage_frame, bg="#383838", width=200, height=50)
                fire_damage_frame.pack(side=tk.LEFT, anchor="w")
                fire_damage_var = tk.DoubleVar()
                tk.Label(fire_damage_frame, text="Fire:", font=("Arial", 14), bg="#C52801", fg="#000000").pack(side=tk.LEFT)
                fire_damage_spinbox = tk.Spinbox(fire_damage_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=fire_damage_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                fire_damage_spinbox.pack(side=tk.RIGHT, padx=5)

                cold_damage_frame = tk.Frame(damage_frame, bg="#383838", width=200, height=50)
                cold_damage_frame.pack(side=tk.LEFT, anchor="w")
                cold_damage_var = tk.DoubleVar()
                tk.Label(cold_damage_frame, text="Cold:", font=("Arial", 14), bg="#005DD6", fg="#000000").pack(side=tk.LEFT)
                cold_damage_spinbox = tk.Spinbox(cold_damage_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=cold_damage_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                cold_damage_spinbox.pack(side=tk.RIGHT, padx=5)

                lightning_damage_frame = tk.Frame(damage_frame, bg="#383838", width=200, height=50)
                lightning_damage_frame.pack(side=tk.LEFT, anchor="w")
                lightning_damage_var = tk.DoubleVar()
                tk.Label(lightning_damage_frame, text="Lightning:", font=("Arial", 14), bg="#FFFB00", fg="#000000").pack(side=tk.LEFT)
                lightning_damage_spinbox = tk.Spinbox(lightning_damage_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=lightning_damage_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                lightning_damage_spinbox.pack(side=tk.RIGHT, padx=5)

                attack_speed_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                attack_speed_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(attack_speed_frame, text="Attack Speed:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
                attack_speed_var = tk.DoubleVar()
                attack_speed_spinbox = tk.Spinbox(attack_speed_frame, from_=0.0, to=10.0, increment=0.1, textvariable=attack_speed_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=28)
                attack_speed_spinbox.pack(side=tk.RIGHT, padx=5)

                crit_chance_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                crit_chance_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(crit_chance_frame, text="Crit Chance:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
                crit_chance_var = tk.DoubleVar()
                crit_chance_spinbox = tk.Spinbox(crit_chance_frame, from_=0.0, to=100.0, increment=0.1, textvariable=crit_chance_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=28)
                crit_chance_spinbox.pack(side=tk.RIGHT, padx=5)

                crit_multiplier_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                crit_multiplier_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(crit_multiplier_frame, text="Crit Multiplier:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
                crit_multiplier_var = tk.DoubleVar()
                crit_multiplier_spinbox = tk.Spinbox(crit_multiplier_frame, from_=0.0, to=10.0, increment=0.1, textvariable=crit_multiplier_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=28)
                crit_multiplier_spinbox.pack(side=tk.RIGHT, padx=5)

                slot_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                slot_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(slot_frame, text="Slot:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
                slot_combobox = ttk.Combobox(slot_frame, values=["Mainhand", "Offhand", "Two-handed"], font=("Arial", 14))
                slot_combobox.pack(side=tk.RIGHT, padx=5)

                durability_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                durability_frame.pack(padx=5, pady=5, anchor="nw")
                tk.Label(durability_frame, text="Durability:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
                durability_var = tk.IntVar()
                durability_spinbox = tk.Spinbox(durability_frame, from_=100, to=100000, increment=1, textvariable=durability_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=10)
                durability_spinbox.pack(padx=5, pady=5, side=tk.LEFT)

                requirements_frame = tk.Frame(resource_frame, bg="#383838", width=800, height=50)
                requirements_frame.pack(pady=5, padx=5, anchor="n")
                tk.Label(requirements_frame, text="Requirements", font=("Arial", 16), bg="#383838", fg="#ffffff").pack(side=tk.TOP, pady=5)
                tk.Label(requirements_frame, text="Level", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT, pady=5)
                level_requirement_var = tk.IntVar()
                level_requirement_spinbox = tk.Spinbox(requirements_frame, from_=1, to=100, increment=1, textvariable=level_requirement_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=5)
                level_requirement_spinbox.pack(side=tk.LEFT, padx=5, pady=5)
                tk.Label(requirements_frame, text="Strength", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT, pady=5)
                strength_requirement_var = tk.IntVar()
                strength_requirement_spinbox = tk.Spinbox(requirements_frame, from_=0, to=100, increment=1, textvariable=strength_requirement_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=5)
                strength_requirement_spinbox.pack(side=tk.LEFT, padx=5, pady=5)
                tk.Label(requirements_frame, text="Agility", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT, pady=5)
                agility_requirement_var = tk.IntVar()
                agility_requirement_spinbox = tk.Spinbox(requirements_frame, from_=0, to=100, increment=1, textvariable=agility_requirement_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=5)
                agility_requirement_spinbox.pack(side=tk.LEFT, padx=5, pady=5)
                tk.Label(requirements_frame, text="Intelligence", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT, pady=5)
                intelligence_requirement_var = tk.IntVar()
                intelligence_requirement_spinbox = tk.Spinbox(requirements_frame, from_=0, to=100, increment=1, textvariable=intelligence_requirement_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=5)
                intelligence_requirement_spinbox.pack(side=tk.LEFT, padx=5, pady=5)

            elif item_type == "Armor":
                # TODO load armor specific fields
                print("armor")
                pass
            elif item_type == "Jewelry":
                # TODO load jewelry specific fields
                print("jewelry")
                pass
            elif item_type == "Utility":
                # TODO load utility specific fields
                print("utility")
                pass
            elif item_type == "Consumable":
                # TODO load consumable specific fields
                print("consumable")
                pass
            elif item_type == "Materials":
                pass

        self.clear_all_inside_frame(self.root)
        top_frame = tk.Frame(self.root, bg="#2e2e2e", width=800, height=100)
        top_frame.pack(pady=5, padx=5, side=tk.TOP)
        tk.Label(top_frame, text="Item creator", font=("Arial", 24), bg="#2e2e2e", fg="#ffffff").pack()

        main_frame = tk.Frame(self.root, bg="#383838", width=800, height=500)
        main_frame.pack(pady=5, padx=5, anchor="center", expand=True, fill=tk.BOTH)

        bottom_frame = tk.Frame(self.root, bg="#383838", width=800, height=50)
        bottom_frame.pack(pady=5, padx=5, anchor="s", side=tk.BOTTOM)
        tk.Button(bottom_frame, text="Save", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=lambda: save_item()).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Cancel", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=self.start).pack(side=tk.RIGHT, padx=5)

        item_type_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        item_type_frame.pack(pady=5, padx=5, anchor="center")
        tk.Label(item_type_frame, text="Item type:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(pady=5, side=tk.TOP)
        item_type_combobox = ttk.Combobox(item_type_frame, values=["Weapon", "Armor", "Jewelry", "Utility", "Consumable", "Materials"], font=("Arial", 14))
        item_type_combobox.pack(padx=5, side=tk.LEFT)
        confirm_button = tk.Button(item_type_frame, text="Confirm", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=lambda: create_item_fields(item_type_combobox.get(), resource_frame))
        confirm_button.pack(padx=5, side=tk.LEFT)

        name_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        name_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(name_frame, text="Name:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        name_entry = tk.Entry(name_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=30)
        name_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(name_frame, text="Identificator:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        identificator_entry = tk.Entry(name_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=30)
        identificator_entry.pack(side=tk.LEFT, padx=5)

        rarity_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        rarity_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(rarity_frame, text="Rarity:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        rarity_combobox = ttk.Combobox(rarity_frame, values=["Common", "Uncommon", "Rare", "Epic", "Legendary"], font=("Arial", 14))
        rarity_combobox.pack(side=tk.RIGHT, padx=5)

        stackable_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        stackable_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(stackable_frame, text="Stackable:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        stackable_var = tk.BooleanVar(value=False)
        stackable_checkbutton = tk.Checkbutton(stackable_frame, variable=stackable_var, bg="#383838")
        stackable_checkbutton.pack(side=tk.LEFT, padx=5)

        value_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        value_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(value_frame, text="Ценность предмета:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        value_var = tk.IntVar()
        value_spinbox = tk.Spinbox(value_frame, from_=0, to=100, increment=1, textvariable=value_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
        value_spinbox.pack(side=tk.LEFT, padx=5)

        resource_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        resource_frame.pack(pady=5, padx=5, anchor="nw")

        description_frame = tk.Frame(main_frame, bg="#383838", width=800, height=100)
        description_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(description_frame, text="Description:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.TOP, anchor="w")
        description_text = tk.Text(description_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=60, height=5)
        description_text.pack(side=tk.BOTTOM, padx=5, pady=5)


    def create_entity(self):
        def save_entity():
            if not self.resource_type:
                return
            entity_name = entity_name_entry.get()
            entity_type = entity_type_combobox.get()
            entity_description = description_text.get("1.0", "end-1c")
            file_name = file_name_entry.get() + ".json"
            if not all([entity_name, entity_type, entity_description, file_name]):
                self.show_error("Одно из обязательных полей не заполнено!")
                return
            if self.resource_type == "Enemy":
                from game.classes.entity import Enemy
                entity_damage = damage_var.get()
                entity_armor = armor_rating_var.get()
                entity_health = health_var.get()
                entity_fire_resistance = fire_resistance_var.get()
                entity_cold_resistance = cold_resistance_var.get()
                entity_lightning_resistance = lightning_resistance_var.get()
                entity_strength = strength_var.get()
                entity_agility = agility_var.get()
                entity_intelligence = intelligence_var.get()
                entity_drop = drop_listbox.get("0", "end")
                drop = []
                for item_drop in entity_drop:
                    item_id, max_count = item_drop.split(":")
                    item = game_manager.get_item(int(item_id))
                    drop.append([item, int(max_count)])
                data = {
                    "base_hp": entity_health,
                    "entity_type": entity_type,
                    "name": entity_name,
                    "damage": entity_damage,
                    "armor": entity_armor,
                    "description": entity_description,
                    "drop": drop
                }
                enemy = Enemy(data=data)
                enemy.attributes.set(strength=entity_strength, agility=entity_agility, intelligence=entity_intelligence)
                enemy.characteristics.resistances.set(entity_fire_resistance, entity_cold_resistance, entity_lightning_resistance)

                enemy_json = enemy.to_dict()
                with open(file=RESOURCES_DIR / "entity" / "enemy" / file_name, mode="w", encoding="utf-8") as file:
                    json.dump(enemy_json, file, indent=6)
                
            elif self.resource_type == "NPC":
                ...
            else:
                return


        def create_entity_fields(entity_type, resource_frame: Frame):
            self.clear_all_inside_frame(resource_frame)
            if not entity_type:
                return
            if resource_frame.winfo_children():
                return
            self.resource_type = entity_type
            if entity_type == "Enemy":
                global damage_var,armor_rating_var, health_var, fire_resistance_var, cold_resistance_var, lightning_resistance_var, strength_var, agility_var, intelligence_var, drop_listbox
                # TODO load enemy specific fields

                # ------------------------------------------------------------------------------------
                # characteristics
                characteristics_frame = tk.Frame(resource_frame, bg="#424242", width=800, height=50)
                characteristics_frame.pack(pady=5, padx=5, anchor="n", expand=True, fill=tk.X)
                tk.Label(characteristics_frame, text="Characteristics:", font=("Arial", 16), bg="#424242", fg="#ffffff").pack(side=tk.TOP)

                damage_frame = tk.Frame(characteristics_frame, bg="#424242", width=800, height=50)
                damage_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(damage_frame, text="Base damage:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(side=tk.LEFT)
                damage_var = tk.DoubleVar()
                damage_spinbox = tk.Spinbox(damage_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=damage_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=28)
                damage_spinbox.pack(side=tk.RIGHT, padx=5)

                armor_rating_frame = tk.Frame(characteristics_frame, bg="#424242", width=800, height=50)
                armor_rating_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(armor_rating_frame, text="Armor Rating:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(side=tk.LEFT)
                armor_rating_var = tk.DoubleVar()
                armor_rating_spinbox = tk.Spinbox(armor_rating_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=armor_rating_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=28)
                armor_rating_spinbox.pack(side=tk.LEFT, padx=5)

                health_frame = tk.Frame(characteristics_frame, bg="#424242", width=800, height=50)
                health_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(health_frame, text="Base Health:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(side=tk.LEFT)
                health_var = tk.DoubleVar()
                health_spinbox = tk.Spinbox(health_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=health_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=28)
                health_spinbox.pack(side=tk.RIGHT, padx=5)

                resistances_frame = tk.Frame(characteristics_frame, bg="#424242", width=800, height=50)
                resistances_frame.pack(pady=5, padx=5, anchor="nw")
                tk.Label(resistances_frame, text="Resistances:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(side=tk.LEFT)

                fire_resistance_frame = tk.Frame(resistances_frame, bg="#424242", width=200, height=50)
                fire_resistance_frame.pack(side=tk.LEFT, anchor="w")
                tk.Label(fire_resistance_frame, text="Fire:", font=("Arial", 14), bg="#C52801", fg="#000000").pack(side=tk.LEFT)
                fire_resistance_var = tk.DoubleVar()
                fire_resistance_spinbox = tk.Spinbox(fire_resistance_frame, from_=0.0, to=100.0, increment=0.1, textvariable=fire_resistance_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                fire_resistance_spinbox.pack(side=tk.RIGHT, padx=5)

                cold_resistance_frame = tk.Frame(resistances_frame, bg="#424242", width=200, height=50)
                cold_resistance_frame.pack(side=tk.LEFT, anchor="w")
                tk.Label(cold_resistance_frame, text="Cold:", font=("Arial", 14), bg="#005DD6", fg="#000000").pack(side=tk.LEFT)
                cold_resistance_var = tk.DoubleVar()
                cold_resistance_spinbox = tk.Spinbox(cold_resistance_frame, from_=0.0, to=100.0, increment=0.1, textvariable=cold_resistance_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                cold_resistance_spinbox.pack(side=tk.RIGHT, padx=5)

                lightning_resistance_frame = tk.Frame(resistances_frame, bg="#424242", width=200, height=50)
                lightning_resistance_frame.pack(side=tk.LEFT, anchor="w")
                tk.Label(lightning_resistance_frame, text="Lightning:", font=("Arial", 14), bg="#FFFB00", fg="#000000").pack(side=tk.LEFT)
                lightning_resistance_var = tk.DoubleVar()
                lightning_resistance_spinbox = tk.Spinbox(lightning_resistance_frame, from_=0.0, to=100.0, increment=0.1, textvariable=lightning_resistance_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                lightning_resistance_spinbox.pack(side=tk.RIGHT, padx=5)

                start_attributes_frame = tk.Frame(characteristics_frame, bg="#424242", width=800, height=50)
                start_attributes_frame.pack(pady=5, padx=5, anchor="n", expand=True, fill=tk.X)
                tk.Label(start_attributes_frame, text="Start Attributes", font=("Arial", 16), bg="#424242", fg="#ffffff").pack(padx=5, pady=5, side=tk.TOP)
                # strength
                strength_frame = tk.Frame(start_attributes_frame, bg="#424242", width=800, height=50)
                strength_frame.pack(pady=5, padx=5, side=tk.LEFT, fill=tk.X)
                tk.Label(strength_frame, text="Strength:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(padx=5, pady=5, side=tk.LEFT)
                strength_var = tk.IntVar()
                strength_spinbox = tk.Spinbox(strength_frame, from_=0, to=1000, increment=1, textvariable=strength_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                strength_spinbox.pack(padx=5, pady=5, side=tk.LEFT)
                # agility
                agility_frame = tk.Frame(start_attributes_frame, bg="#424242", width=800, height=50)
                agility_frame.pack(pady=5, padx=5, side=tk.LEFT, fill=tk.X)
                tk.Label(agility_frame, text="Agility:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(padx=5, pady=5, side=tk.LEFT)
                agility_var = tk.IntVar()
                agility_spinbox = tk.Spinbox(agility_frame, from_=0, to=1000, increment=1, textvariable=agility_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                agility_spinbox.pack(padx=5, pady=5, side=tk.LEFT)
                #intelligence
                intelligence_frame = tk.Frame(start_attributes_frame, bg="#424242", width=800, height=50)
                intelligence_frame.pack(pady=5, padx=5, side=tk.LEFT, fill=tk.X)
                tk.Label(intelligence_frame, text="Intelligence:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(padx=5, pady=5, side=tk.LEFT)
                intelligence_var = tk.IntVar()
                intelligence_spinbox = tk.Spinbox(intelligence_frame, from_=0, to=1000, increment=1, textvariable=intelligence_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                intelligence_spinbox.pack(padx=5, pady=5, side=tk.LEFT)

                # characteristics
                # ------------------------------------------------------------------------------------
                # drop
                drop_frame = tk.Frame(resource_frame, bg="#424242", width=800, height=50)
                drop_frame.pack(pady=5, padx=5, anchor="nw", side=tk.LEFT)
                tk.Label(drop_frame, text="Drop:", font=("Arial", 16), bg="#424242", fg="#ffffff").pack(side=tk.TOP)
                drop_listbox = tk.Listbox(drop_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=30, height=5)
                drop_listbox.pack(side=tk.LEFT, padx=5)

                add_drop_frame = tk.Frame(drop_frame, bg="#424242", width=800, height=100)
                add_drop_frame.pack(pady=5, padx=5  , anchor="nw", side=tk.TOP, expand=True, fill=tk.BOTH)

                item_id_frame = tk.Frame(add_drop_frame, bg="#424242", width=200, height=50)
                item_id_frame.pack(side=tk.TOP)
                tk.Label(item_id_frame, text="Item ID:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(side=tk.LEFT)
                item_id_var = tk.IntVar()
                item_id_spinbox = tk.Spinbox(item_id_frame, from_=0, to=10000, increment=1, textvariable=item_id_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                item_id_spinbox.pack(side=tk.RIGHT, padx=5)

                count_frame = tk.Frame(add_drop_frame, bg="#424242", width=200, height=50)
                count_frame.pack(side=tk.TOP)
                tk.Label(count_frame, text="Count:", font=("Arial", 14), bg="#424242", fg="#ffffff").pack(side=tk.LEFT)
                count_var = tk.IntVar()
                count_spinbox = tk.Spinbox(count_frame, from_=1, to=1000, increment=1, textvariable=count_var, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=8)
                count_spinbox.pack(side=tk.RIGHT, padx=5)

                add_drop_button = tk.Button(add_drop_frame, text="Add Drop", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", command=lambda: drop_listbox.insert(tk.END, f"{item_id_var.get()}:{count_var.get()}"))
                add_drop_button.pack(side=tk.TOP, padx=5, pady=5)

                remove_drop_button = tk.Button(add_drop_frame, text="Remove Selected Drop", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", command=lambda: drop_listbox.delete(drop_listbox.curselection()))
                remove_drop_button.pack(side=tk.TOP, padx=5, pady=5)
                # drop
                # ------------------------------------------------------------------------------------
                
            elif entity_type == "NPC":
                # TODO load NPC specific fields
                print("npc")
                pass

        self.clear_all_inside_frame(self.root)
        top_frame = tk.Frame(self.root, bg="#2e2e2e", width=800, height=100)
        top_frame.pack(pady=5, side=tk.TOP)
        tk.Label(top_frame, text="Entity creator", font=("Arial", 24), bg="#2e2e2e", fg="#ffffff").pack()

        main_frame = tk.Frame(self.root, bg="#383838", width=800, height=500)
        main_frame.pack(pady=5, padx=5, anchor="center", expand=True, fill=tk.BOTH)

        bottom_frame = tk.Frame(self.root, bg="#383838", width=800, height=50)
        bottom_frame.pack(pady=5, padx=5, anchor="s", side=tk.BOTTOM)
        tk.Button(bottom_frame, text="Save", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=lambda: save_entity()).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Cancel", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=self.start).pack(side=tk.RIGHT, padx=5)

        entity_type_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        entity_type_frame.pack(pady=5, padx=5, anchor="n")
        tk.Label(entity_type_frame, text="Entity type:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.TOP, pady=5)
        entity_type_combobox = ttk.Combobox(entity_type_frame, values=["Enemy", "NPC"], font=("Arial", 14))
        entity_type_combobox.pack(side=tk.LEFT, padx=5)
        confirm_button = tk.Button(entity_type_frame, text="Confirm", font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=20, command=lambda: create_entity_fields(entity_type_combobox.get(), resource_frame))
        confirm_button.pack(side=tk.LEFT, padx=5)

        entity_name_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        entity_name_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(entity_name_frame, text="Name:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        entity_name_entry = tk.Entry(entity_name_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=30)
        entity_name_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(entity_name_frame, text="File Name:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)
        file_name_entry = tk.Entry(entity_name_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=30)
        file_name_entry.pack(side=tk.LEFT)
        tk.Label(entity_name_frame, text=".json", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.LEFT)


        resource_frame = tk.Frame(main_frame, bg="#383838", width=800, height=50)
        resource_frame.pack(pady=5, padx=5, anchor="nw")

        description_frame = tk.Frame(main_frame, bg="#383838", width=800, height=100)
        description_frame.pack(pady=5, padx=5, anchor="nw")
        tk.Label(description_frame, text="Description:", font=("Arial", 14), bg="#383838", fg="#ffffff").pack(side=tk.TOP, anchor="w")
        description_text = tk.Text(description_frame, font=("Arial", 14), bg="#4a4a4a", fg="#ffffff", width=60, height=5)
        description_text.pack(side=tk.BOTTOM, padx=5, pady=5)

    def create_quest(self):
        ...

    def show_resources(self):
        ...

    def clear_all_inside_frame(self, frame: Frame | Tk):
        # Iterate through every widget inside the frame
        for widget in frame.winfo_children():
            widget.destroy()  # deleting widget


if __name__ == "__main__":
    app = ResourceCreator()
    app.start()