# gamification.py
import streamlit as st
import time
from collections import defaultdict

class Gamification:
    """
    Gamification system for Earthify waste detection app.
    Handles scoring, achievements, and environmental impact tracking.
    """

    def __init__(self):
        # Initialize session state variables if not exists
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'total_detections' not in st.session_state:
            st.session_state.total_detections = 0
        if 'achievements' not in st.session_state:
            st.session_state.achievements = set()
        if 'environmental_impact' not in st.session_state:
            st.session_state.environmental_impact = {
                'landfill_diverted_kg': 0.0,
                'co2_saved_kg': 0.0,
                'trees_saved': 0,
                'energy_saved_kwh': 0.0
            }
        if 'detection_history' not in st.session_state:
            st.session_state.detection_history = defaultdict(int)
        if 'last_achievement_check' not in st.session_state:
            st.session_state.last_achievement_check = time.time()

    # Scoring system
    POINTS_SYSTEM = {
        'recyclable': 10,
        'non_recyclable': 5,
        'hazardous': 20
    }

    # Environmental impact per item (approximate values)
    IMPACT_SYSTEM = {
        'recyclable': {
            'landfill_diverted_kg': 0.5,
            'co2_saved_kg': 1.2,
            'trees_saved': 0.01,  # fraction of tree saved
            'energy_saved_kwh': 2.5
        },
        'non_recyclable': {
            'landfill_diverted_kg': 0.1,
            'co2_saved_kg': 0.3,
            'trees_saved': 0.002,
            'energy_saved_kwh': 0.5
        },
        'hazardous': {
            'landfill_diverted_kg': 1.0,
            'co2_saved_kg': 2.0,
            'trees_saved': 0.02,
            'energy_saved_kwh': 5.0
        }
    }

    # Achievement definitions
    ACHIEVEMENTS = {
        'first_detection': {
            'condition': lambda self: st.session_state.total_detections >= 1,
            'name': '🗑️ First Detection',
            'description': 'Detected your first waste item!'
        },
        'recycle_hero': {
            'condition': lambda self: st.session_state.detection_history.get('recyclable', 0) >= 10,
            'name': '♻️ Recycle Hero',
            'description': 'Detected 10 recyclable items'
        },
        'hazard_hunter': {
            'condition': lambda self: st.session_state.detection_history.get('hazardous', 0) >= 5,
            'name': '⚠️ Hazard Hunter',
            'description': 'Detected 5 hazardous items'
        },
        'eco_warrior': {
            'condition': lambda self: st.session_state.score >= 100,
            'name': '🌍 Eco Warrior',
            'description': 'Earned 100 points'
        },
        'master_sorter': {
            'condition': lambda self: st.session_state.total_detections >= 50,
            'name': '🏆 Master Sorter',
            'description': 'Detected 50 waste items total'
        },
        'carbon_saver': {
            'condition': lambda self: st.session_state.environmental_impact['co2_saved_kg'] >= 10,
            'name': '🌱 Carbon Saver',
            'description': 'Saved 10kg of CO2 emissions'
        }
    }

    def add_detection(self, item_type, item_name):
        """
        Add a detection event to the gamification system.

        Args:
            item_type (str): 'recyclable', 'non_recyclable', or 'hazardous'
            item_name (str): The specific item detected
        """
        # Add points
        points = self.POINTS_SYSTEM.get(item_type, 0)
        st.session_state.score += points

        # Update detection counts
        st.session_state.total_detections += 1
        st.session_state.detection_history[item_type] += 1

        # Update environmental impact
        impact = self.IMPACT_SYSTEM.get(item_type, {})
        for key, value in impact.items():
            st.session_state.environmental_impact[key] += value

        # Check for new achievements (throttle to avoid spam)
        current_time = time.time()
        if current_time - st.session_state.last_achievement_check > 1.0:  # Check every second
            self._check_achievements()
            st.session_state.last_achievement_check = current_time

    def _check_achievements(self):
        """Check and unlock new achievements."""
        new_achievements = []
        for ach_id, ach_data in self.ACHIEVEMENTS.items():
            if ach_id not in st.session_state.achievements and ach_data['condition'](self):
                st.session_state.achievements.add(ach_id)
                new_achievements.append(ach_data)

        return new_achievements

    def get_new_achievements(self):
        """Get list of newly unlocked achievements since last check."""
        return self._check_achievements()

    def display_stats(self):
        """Display gamification stats in Streamlit sidebar."""
        st.sidebar.markdown("---")
        st.sidebar.subheader("🏆 Your Eco Impact")

        # Score
        st.sidebar.metric("Total Score", f"{st.session_state.score} pts")

        # Detections
        col1, col2, col3 = st.sidebar.columns(3)
        with col1:
            st.metric("♻️ Recyclable", st.session_state.detection_history.get('recyclable', 0))
        with col2:
            st.metric("🗑️ Non-Recyclable", st.session_state.detection_history.get('non_recyclable', 0))
        with col3:
            st.metric("⚠️ Hazardous", st.session_state.detection_history.get('hazardous', 0))

        # Environmental Impact
        st.sidebar.markdown("### 🌍 Environmental Impact")
        impact = st.session_state.environmental_impact
        st.sidebar.write(f"**Landfill Diverted:** {impact['landfill_diverted_kg']:.1f} kg")
        st.sidebar.write(f"**CO2 Saved:** {impact['co2_saved_kg']:.1f} kg")
        st.sidebar.write(f"**Trees Saved:** {impact['trees_saved']:.2f}")
        st.sidebar.write(f"**Energy Saved:** {impact['energy_saved_kwh']:.1f} kWh")

        # Achievements
        if st.session_state.achievements:
            st.sidebar.markdown("### 🏅 Achievements")
            for ach_id in sorted(st.session_state.achievements):
                ach_data = self.ACHIEVEMENTS[ach_id]
                st.sidebar.write(f"**{ach_data['name']}**")
                st.sidebar.caption(ach_data['description'])
        else:
            st.sidebar.markdown("### 🏅 Achievements")
            st.sidebar.caption("No achievements yet. Start detecting waste!")

    def reset_stats(self):
        """Reset all gamification stats (for testing or new session)."""
        st.session_state.score = 0
        st.session_state.total_detections = 0
        st.session_state.achievements = set()
        st.session_state.environmental_impact = {
            'landfill_diverted_kg': 0.0,
            'co2_saved_kg': 0.0,
            'trees_saved': 0,
            'energy_saved_kwh': 0.0
        }
        st.session_state.detection_history = defaultdict(int)
        st.session_state.last_achievement_check = time.time()

    def get_summary(self):
        """Get a summary of current stats for API or logging."""
        return {
            'score': st.session_state.score,
            'total_detections': st.session_state.total_detections,
            'detection_breakdown': dict(st.session_state.detection_history),
            'achievements': list(st.session_state.achievements),
            'environmental_impact': st.session_state.environmental_impact.copy()
        }

# Global instance for easy access
gamification = Gamification()