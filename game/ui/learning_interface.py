"""
Enhanced Learning Interface - Interactive educational content
"""

import pygame
from typing import Dict, List, Optional, Tuple
from enum import Enum

class LearningPhase(Enum):
    """Phases of the learning process"""
    INTRODUCTION = "introduction"
    CONTENT = "content"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    PRACTICAL = "practical"
    SUMMARY = "summary"

class InteractiveLearningUI:
    """Enhanced learning interface with multiple phases"""
    
    def __init__(self):
        self.font_title = pygame.font.Font(None, 36)
        self.font_content = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        # Learning state
        self.current_phase = LearningPhase.INTRODUCTION
        self.current_concept = None
        self.current_page = 0
        self.total_pages = 0
        self.quiz_score = 0
        self.quiz_attempts = 0
        
        # Interactive elements
        self.selected_option = 0
        self.user_answers = {}
        self.practical_completed = False
        
        # Colors
        self.bg_color = (15, 25, 40)
        self.panel_color = (30, 45, 70)
        self.accent_color = (100, 150, 255)
        self.success_color = (50, 200, 50)
        self.warning_color = (255, 150, 50)
        self.error_color = (255, 50, 50)
    
    def start_learning(self, concept):
        """Start the enhanced learning process"""
        self.current_concept = concept
        self.current_phase = LearningPhase.INTRODUCTION
        self.current_page = 0
        self.quiz_score = 0
        self.quiz_attempts = 0
        self.user_answers.clear()
        self.practical_completed = False
        
        # Calculate total pages based on content
        self.total_pages = self._calculate_total_pages(concept)
    
    def _calculate_total_pages(self, concept) -> int:
        """Calculate total pages for the concept"""
        pages = 1  # Introduction
        
        # Content pages (split long content)
        content_length = len(concept.detailed_content)
        pages += max(1, content_length // 800)  # ~800 chars per page
        
        pages += 1  # Interactive demonstration
        pages += len(self._get_quiz_questions(concept.id))  # Quiz questions
        pages += 1  # Practical exercise
        pages += 1  # Summary
        
        return pages
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input for the learning interface"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False  # Close learning interface
            
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                return self._advance_phase()
            
            elif event.key == pygame.K_LEFT:
                return self._previous_phase()
            
            elif event.key == pygame.K_UP:
                self.selected_option = max(0, self.selected_option - 1)
                return True
            
            elif event.key == pygame.K_DOWN:
                max_options = self._get_max_options()
                self.selected_option = min(max_options - 1, self.selected_option + 1)
                return True
            
            elif event.key == pygame.K_RETURN:
                return self._handle_selection()
        
        return True
    
    def _advance_phase(self) -> bool:
        """Advance to next phase or page"""
        if self.current_phase == LearningPhase.INTRODUCTION:
            self.current_phase = LearningPhase.CONTENT
            
        elif self.current_phase == LearningPhase.CONTENT:
            if self.current_page < self._get_content_pages() - 1:
                self.current_page += 1
            else:
                self.current_phase = LearningPhase.INTERACTIVE
                self.current_page = 0
                
        elif self.current_phase == LearningPhase.INTERACTIVE:
            self.current_phase = LearningPhase.QUIZ
            self.current_page = 0
            
        elif self.current_phase == LearningPhase.QUIZ:
            questions = self._get_quiz_questions(self.current_concept.id)
            if self.current_page < len(questions) - 1:
                self.current_page += 1
                self.selected_option = 0
            else:
                self.current_phase = LearningPhase.PRACTICAL
                self.current_page = 0
                
        elif self.current_phase == LearningPhase.PRACTICAL:
            if self.practical_completed:
                self.current_phase = LearningPhase.SUMMARY
                
        elif self.current_phase == LearningPhase.SUMMARY:
            return False  # Complete learning
        
        return True
    
    def _previous_phase(self) -> bool:
        """Go back to previous phase or page"""
        if self.current_page > 0:
            self.current_page -= 1
        elif self.current_phase == LearningPhase.CONTENT:
            self.current_phase = LearningPhase.INTRODUCTION
        elif self.current_phase == LearningPhase.INTERACTIVE:
            self.current_phase = LearningPhase.CONTENT
            self.current_page = self._get_content_pages() - 1
        elif self.current_phase == LearningPhase.QUIZ:
            self.current_phase = LearningPhase.INTERACTIVE
        elif self.current_phase == LearningPhase.PRACTICAL:
            self.current_phase = LearningPhase.QUIZ
            self.current_page = len(self._get_quiz_questions(self.current_concept.id)) - 1
        elif self.current_phase == LearningPhase.SUMMARY:
            self.current_phase = LearningPhase.PRACTICAL
        
        return True
    
    def _handle_selection(self) -> bool:
        """Handle selection in current phase"""
        if self.current_phase == LearningPhase.QUIZ:
            return self._handle_quiz_answer()
        elif self.current_phase == LearningPhase.PRACTICAL:
            return self._handle_practical_action()
        
        return True
    
    def _handle_quiz_answer(self) -> bool:
        """Handle quiz answer selection"""
        questions = self._get_quiz_questions(self.current_concept.id)
        if self.current_page < len(questions):
            question = questions[self.current_page]
            self.user_answers[self.current_page] = self.selected_option
            
            if self.selected_option == question['correct']:
                self.quiz_score += 1
            
            self.quiz_attempts += 1
        
        return True
    
    def _handle_practical_action(self) -> bool:
        """Handle practical exercise actions"""
        # Simulate completing practical exercise
        if self.selected_option == 0:  # "Complete Exercise"
            self.practical_completed = True
        
        return True
    
    def render(self, screen: pygame.Surface):
        """Render the learning interface"""
        # Full screen overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(240)
        overlay.fill(self.bg_color)
        screen.blit(overlay, (0, 0))
        
        # Main panel
        panel_width = min(900, screen.get_width() - 40)
        panel_height = min(650, screen.get_height() - 40)
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = (screen.get_height() - panel_height) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, self.panel_color, panel_rect)
        pygame.draw.rect(screen, self.accent_color, panel_rect, 3)
        
        # Render content based on current phase
        if self.current_phase == LearningPhase.INTRODUCTION:
            self._render_introduction(screen, panel_rect)
        elif self.current_phase == LearningPhase.CONTENT:
            self._render_content(screen, panel_rect)
        elif self.current_phase == LearningPhase.INTERACTIVE:
            self._render_interactive(screen, panel_rect)
        elif self.current_phase == LearningPhase.QUIZ:
            self._render_quiz(screen, panel_rect)
        elif self.current_phase == LearningPhase.PRACTICAL:
            self._render_practical(screen, panel_rect)
        elif self.current_phase == LearningPhase.SUMMARY:
            self._render_summary(screen, panel_rect)
        
        # Progress bar
        self._render_progress_bar(screen, panel_rect)
        
        # Navigation instructions
        self._render_navigation(screen, panel_rect)
    
    def _render_introduction(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render introduction phase"""
        y_offset = panel_rect.y + 40
        
        # Title
        title = f"Learning: {self.current_concept.name}"
        title_surface = self.font_title.render(title, True, self.accent_color)
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, y=y_offset)
        screen.blit(title_surface, title_rect)
        y_offset += 60
        
        # Category
        category_text = f"Category: {self.current_concept.category.value.title()}"
        category_surface = self.font_content.render(category_text, True, (200, 200, 200))
        screen.blit(category_surface, (panel_rect.x + 40, y_offset))
        y_offset += 40
        
        # Description
        desc_surface = self.font_content.render(self.current_concept.description, True, (255, 255, 255))
        screen.blit(desc_surface, (panel_rect.x + 40, y_offset))
        y_offset += 60
        
        # Learning objectives
        objectives_title = self.font_content.render("What you'll learn:", True, self.accent_color)
        screen.blit(objectives_title, (panel_rect.x + 40, y_offset))
        y_offset += 30
        
        objectives = self._get_learning_objectives(self.current_concept.id)
        for objective in objectives:
            obj_text = f"• {objective}"
            obj_surface = self.font_small.render(obj_text, True, (200, 255, 200))
            screen.blit(obj_surface, (panel_rect.x + 60, y_offset))
            y_offset += 25
        
        # Estimated time
        y_offset += 20
        time_text = "Estimated time: 5-8 minutes"
        time_surface = self.font_small.render(time_text, True, (255, 200, 100))
        screen.blit(time_surface, (panel_rect.x + 40, y_offset))
    
    def _render_content(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render content phase with detailed information"""
        y_offset = panel_rect.y + 40
        
        # Title
        title = f"{self.current_concept.name} - Detailed Content"
        title_surface = self.font_title.render(title, True, self.accent_color)
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, y=y_offset)
        screen.blit(title_surface, title_rect)
        y_offset += 50
        
        # Content sections
        content_sections = self._get_content_sections(self.current_concept.id, self.current_page)
        
        for section_title, section_content in content_sections.items():
            # Section title
            section_surface = self.font_content.render(section_title, True, self.accent_color)
            screen.blit(section_surface, (panel_rect.x + 40, y_offset))
            y_offset += 35
            
            # Section content
            lines = self._wrap_text(section_content, panel_rect.width - 80)
            for line in lines[:12]:  # Limit lines per page
                line_surface = self.font_small.render(line, True, (255, 255, 255))
                screen.blit(line_surface, (panel_rect.x + 60, y_offset))
                y_offset += 22
            
            y_offset += 15
    
    def _render_interactive(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render interactive demonstration"""
        y_offset = panel_rect.y + 40
        
        # Title
        title = f"Interactive Demo: {self.current_concept.name}"
        title_surface = self.font_title.render(title, True, self.accent_color)
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, y=y_offset)
        screen.blit(title_surface, title_rect)
        y_offset += 60
        
        # Interactive content based on concept
        demo_content = self._get_interactive_demo(self.current_concept.id)
        
        for item in demo_content:
            if item['type'] == 'text':
                text_surface = self.font_content.render(item['content'], True, (255, 255, 255))
                screen.blit(text_surface, (panel_rect.x + 40, y_offset))
                y_offset += 30
            
            elif item['type'] == 'diagram':
                # Simple diagram representation
                self._render_simple_diagram(screen, panel_rect.x + 40, y_offset, item['content'])
                y_offset += 150
            
            elif item['type'] == 'code':
                # Code example
                code_bg = pygame.Rect(panel_rect.x + 40, y_offset, panel_rect.width - 80, 100)
                pygame.draw.rect(screen, (20, 20, 30), code_bg)
                pygame.draw.rect(screen, self.accent_color, code_bg, 2)
                
                code_lines = item['content'].split('\n')
                for i, line in enumerate(code_lines[:4]):
                    code_surface = self.font_small.render(line, True, (150, 255, 150))
                    screen.blit(code_surface, (panel_rect.x + 50, y_offset + 10 + i * 20))
                
                y_offset += 120
    
    def _render_quiz(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render quiz phase"""
        questions = self._get_quiz_questions(self.current_concept.id)
        if self.current_page >= len(questions):
            return
        
        question = questions[self.current_page]
        y_offset = panel_rect.y + 40
        
        # Title
        title = f"Quiz Question {self.current_page + 1} of {len(questions)}"
        title_surface = self.font_title.render(title, True, self.accent_color)
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, y=y_offset)
        screen.blit(title_surface, title_rect)
        y_offset += 60
        
        # Question
        question_lines = self._wrap_text(question['question'], panel_rect.width - 80)
        for line in question_lines:
            q_surface = self.font_content.render(line, True, (255, 255, 255))
            screen.blit(q_surface, (panel_rect.x + 40, y_offset))
            y_offset += 30
        
        y_offset += 20
        
        # Options
        for i, option in enumerate(question['options']):
            option_color = self.accent_color if i == self.selected_option else (200, 200, 200)
            
            # Selection indicator
            if i == self.selected_option:
                indicator = "► "
            else:
                indicator = "   "
            
            option_text = f"{indicator}{chr(65 + i)}. {option}"
            option_surface = self.font_content.render(option_text, True, option_color)
            screen.blit(option_surface, (panel_rect.x + 60, y_offset))
            y_offset += 35
        
        # Show answer if already answered
        if self.current_page in self.user_answers:
            y_offset += 20
            user_answer = self.user_answers[self.current_page]
            correct_answer = question['correct']
            
            if user_answer == correct_answer:
                result_text = "✓ Correct!"
                result_color = self.success_color
            else:
                result_text = f"✗ Incorrect. Correct answer: {chr(65 + correct_answer)}"
                result_color = self.error_color
            
            result_surface = self.font_content.render(result_text, True, result_color)
            screen.blit(result_surface, (panel_rect.x + 40, y_offset))
            
            # Explanation
            y_offset += 40
            exp_lines = self._wrap_text(question['explanation'], panel_rect.width - 80)
            for line in exp_lines:
                exp_surface = self.font_small.render(line, True, (200, 200, 255))
                screen.blit(exp_surface, (panel_rect.x + 40, y_offset))
                y_offset += 22
    
    def _render_practical(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render practical exercise"""
        y_offset = panel_rect.y + 40
        
        # Title
        title = f"Practical Exercise: {self.current_concept.name}"
        title_surface = self.font_title.render(title, True, self.accent_color)
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, y=y_offset)
        screen.blit(title_surface, title_rect)
        y_offset += 60
        
        # Exercise content
        exercise = self._get_practical_exercise(self.current_concept.id)
        
        # Scenario
        scenario_title = self.font_content.render("Scenario:", True, self.accent_color)
        screen.blit(scenario_title, (panel_rect.x + 40, y_offset))
        y_offset += 30
        
        scenario_lines = self._wrap_text(exercise['scenario'], panel_rect.width - 80)
        for line in scenario_lines:
            line_surface = self.font_small.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (panel_rect.x + 60, y_offset))
            y_offset += 22
        
        y_offset += 30
        
        # Task
        task_title = self.font_content.render("Your Task:", True, self.accent_color)
        screen.blit(task_title, (panel_rect.x + 40, y_offset))
        y_offset += 30
        
        task_lines = self._wrap_text(exercise['task'], panel_rect.width - 80)
        for line in task_lines:
            line_surface = self.font_small.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (panel_rect.x + 60, y_offset))
            y_offset += 22
        
        y_offset += 40
        
        # Actions
        actions = ["Complete Exercise", "Skip Exercise"]
        for i, action in enumerate(actions):
            action_color = self.accent_color if i == self.selected_option else (200, 200, 200)
            
            if i == self.selected_option:
                indicator = "► "
            else:
                indicator = "   "
            
            action_text = f"{indicator}{action}"
            action_surface = self.font_content.render(action_text, True, action_color)
            screen.blit(action_surface, (panel_rect.x + 60, y_offset))
            y_offset += 35
        
        # Show completion status
        if self.practical_completed:
            y_offset += 20
            completion_text = "✓ Exercise completed successfully!"
            completion_surface = self.font_content.render(completion_text, True, self.success_color)
            screen.blit(completion_surface, (panel_rect.x + 40, y_offset))
    
    def _render_summary(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render learning summary"""
        y_offset = panel_rect.y + 40
        
        # Title
        title = f"Learning Complete: {self.current_concept.name}"
        title_surface = self.font_title.render(title, True, self.success_color)
        title_rect = title_surface.get_rect(centerx=panel_rect.centerx, y=y_offset)
        screen.blit(title_surface, title_rect)
        y_offset += 60
        
        # Quiz results
        quiz_questions = self._get_quiz_questions(self.current_concept.id)
        quiz_percentage = (self.quiz_score / len(quiz_questions)) * 100 if quiz_questions else 0
        
        score_text = f"Quiz Score: {self.quiz_score}/{len(quiz_questions)} ({quiz_percentage:.0f}%)"
        score_color = self.success_color if quiz_percentage >= 70 else self.warning_color
        score_surface = self.font_content.render(score_text, True, score_color)
        screen.blit(score_surface, (panel_rect.x + 40, y_offset))
        y_offset += 40
        
        # Practical status
        practical_text = "Practical Exercise: " + ("Completed" if self.practical_completed else "Skipped")
        practical_color = self.success_color if self.practical_completed else self.warning_color
        practical_surface = self.font_content.render(practical_text, True, practical_color)
        screen.blit(practical_surface, (panel_rect.x + 40, y_offset))
        y_offset += 60
        
        # Key takeaways
        takeaways_title = self.font_content.render("Key Takeaways:", True, self.accent_color)
        screen.blit(takeaways_title, (panel_rect.x + 40, y_offset))
        y_offset += 30
        
        takeaways = self._get_key_takeaways(self.current_concept.id)
        for takeaway in takeaways:
            takeaway_text = f"• {takeaway}"
            takeaway_surface = self.font_small.render(takeaway_text, True, (200, 255, 200))
            screen.blit(takeaway_surface, (panel_rect.x + 60, y_offset))
            y_offset += 25
        
        y_offset += 40
        
        # Next steps
        next_title = self.font_content.render("Next Steps:", True, self.accent_color)
        screen.blit(next_title, (panel_rect.x + 40, y_offset))
        y_offset += 30
        
        next_steps = [
            "Practice using this concept in combat",
            "Explore related AWS services",
            "Try the hands-on labs in AWS Console"
        ]
        
        for step in next_steps:
            step_text = f"• {step}"
            step_surface = self.font_small.render(step_text, True, (255, 200, 100))
            screen.blit(step_surface, (panel_rect.x + 60, y_offset))
            y_offset += 25
    
    def _render_progress_bar(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render progress bar"""
        progress_y = panel_rect.y + panel_rect.height - 60
        progress_width = panel_rect.width - 80
        progress_height = 8
        
        # Background
        bg_rect = pygame.Rect(panel_rect.x + 40, progress_y, progress_width, progress_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        
        # Progress
        phase_progress = {
            LearningPhase.INTRODUCTION: 0.1,
            LearningPhase.CONTENT: 0.3,
            LearningPhase.INTERACTIVE: 0.5,
            LearningPhase.QUIZ: 0.7,
            LearningPhase.PRACTICAL: 0.9,
            LearningPhase.SUMMARY: 1.0
        }
        
        progress = phase_progress.get(self.current_phase, 0)
        fill_width = int(progress_width * progress)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(panel_rect.x + 40, progress_y, fill_width, progress_height)
            pygame.draw.rect(screen, self.accent_color, fill_rect)
    
    def _render_navigation(self, screen: pygame.Surface, panel_rect: pygame.Rect):
        """Render navigation instructions"""
        nav_y = panel_rect.y + panel_rect.height - 30
        
        instructions = "SPACE/→: Next | ←: Previous | ↑↓: Select | ENTER: Confirm | ESC: Exit"
        nav_surface = self.font_small.render(instructions, True, (150, 150, 150))
        nav_rect = nav_surface.get_rect(centerx=panel_rect.centerx, y=nav_y)
        screen.blit(nav_surface, nav_rect)
    
    # Helper methods for content generation
    def _get_learning_objectives(self, concept_id: str) -> List[str]:
        """Get learning objectives for a concept"""
        objectives = {
            'ec2_basics': [
                "Understand what EC2 instances are and their use cases",
                "Learn about different instance types and their purposes",
                "Master Auto Scaling concepts and implementation",
                "Practice launching and configuring EC2 instances"
            ],
            's3_storage': [
                "Understand S3 buckets and object storage concepts",
                "Learn about different storage classes and their costs",
                "Master data lifecycle management strategies",
                "Practice setting up S3 buckets with proper security"
            ],
            'vpc_networking': [
                "Understand Virtual Private Cloud architecture",
                "Learn about subnets, route tables, and gateways",
                "Master security groups and network ACLs",
                "Practice designing secure network architectures"
            ],
            'iam_security': [
                "Understand Identity and Access Management principles",
                "Learn about users, groups, roles, and policies",
                "Master the principle of least privilege",
                "Practice implementing secure access controls"
            ],
            'lambda_serverless': [
                "Understand serverless computing concepts",
                "Learn about event-driven architecture",
                "Master Lambda function development and deployment",
                "Practice building serverless applications"
            ]
        }
        return objectives.get(concept_id, ["Learn the fundamentals", "Apply in practice"])
    
    def _get_content_sections(self, concept_id: str, page: int) -> Dict[str, str]:
        """Get content sections for a concept page"""
        all_content = {
            'ec2_basics': {
                0: {
                    "What is EC2?": "Amazon Elastic Compute Cloud (EC2) provides scalable virtual servers in the AWS cloud. Think of it as renting a computer in Amazon's data center that you can access remotely.",
                    "Key Benefits": "EC2 offers flexibility, scalability, and cost-effectiveness. You only pay for what you use, and you can scale up or down based on demand."
                },
                1: {
                    "Instance Types": "EC2 offers various instance types optimized for different use cases: General Purpose (t3, m5), Compute Optimized (c5), Memory Optimized (r5), and Storage Optimized (i3).",
                    "Auto Scaling": "Auto Scaling automatically adjusts the number of EC2 instances based on demand, ensuring optimal performance and cost efficiency."
                }
            },
            's3_storage': {
                0: {
                    "What is S3?": "Amazon Simple Storage Service (S3) is object storage built to store and retrieve any amount of data from anywhere on the web.",
                    "Storage Classes": "S3 offers multiple storage classes: Standard for frequently accessed data, Glacier for archival, and Intelligent-Tiering for automatic cost optimization."
                }
            }
        }
        
        concept_content = all_content.get(concept_id, {})
        return concept_content.get(page, {"Content": "Detailed information about this concept."})
    
    def _get_content_pages(self) -> int:
        """Get number of content pages"""
        return 2  # Default to 2 pages of content
    
    def _get_interactive_demo(self, concept_id: str) -> List[Dict]:
        """Get interactive demonstration content"""
        demos = {
            'ec2_basics': [
                {'type': 'text', 'content': 'Let\'s see how EC2 Auto Scaling works in practice:'},
                {'type': 'diagram', 'content': 'auto_scaling_diagram'},
                {'type': 'text', 'content': 'When traffic increases, Auto Scaling launches new instances:'},
                {'type': 'code', 'content': 'aws autoscaling create-auto-scaling-group \\\n  --auto-scaling-group-name my-asg \\\n  --min-size 1 --max-size 10 \\\n  --desired-capacity 2'}
            ],
            's3_storage': [
                {'type': 'text', 'content': 'Here\'s how S3 lifecycle management works:'},
                {'type': 'diagram', 'content': 's3_lifecycle_diagram'},
                {'type': 'code', 'content': '{\n  "Rules": [{\n    "Transition": {\n      "Days": 30,\n      "StorageClass": "GLACIER"\n    }\n  }]\n}'}
            ]
        }
        return demos.get(concept_id, [{'type': 'text', 'content': 'Interactive demonstration coming soon!'}])
    
    def _get_quiz_questions(self, concept_id: str) -> List[Dict]:
        """Get quiz questions for a concept"""
        questions = {
            'ec2_basics': [
                {
                    'question': 'What does EC2 stand for?',
                    'options': ['Elastic Compute Cloud', 'Enhanced Cloud Computing', 'Enterprise Cloud Container', 'Elastic Container Cloud'],
                    'correct': 0,
                    'explanation': 'EC2 stands for Elastic Compute Cloud, providing scalable virtual servers in the AWS cloud.'
                },
                {
                    'question': 'Which instance type is best for memory-intensive applications?',
                    'options': ['t3 (General Purpose)', 'c5 (Compute Optimized)', 'r5 (Memory Optimized)', 'i3 (Storage Optimized)'],
                    'correct': 2,
                    'explanation': 'R5 instances are memory optimized, designed specifically for memory-intensive workloads.'
                },
                {
                    'question': 'What is the main benefit of Auto Scaling?',
                    'options': ['Reduces costs', 'Automatically adjusts capacity', 'Improves security', 'Increases performance'],
                    'correct': 1,
                    'explanation': 'Auto Scaling automatically adjusts the number of instances based on demand, ensuring optimal performance and cost.'
                }
            ],
            's3_storage': [
                {
                    'question': 'What is Amazon S3 primarily used for?',
                    'options': ['Computing power', 'Object storage', 'Database hosting', 'Network routing'],
                    'correct': 1,
                    'explanation': 'Amazon S3 is primarily an object storage service for storing and retrieving data.'
                },
                {
                    'question': 'Which S3 storage class is most cost-effective for long-term archival?',
                    'options': ['S3 Standard', 'S3 Intelligent-Tiering', 'S3 Glacier', 'S3 Glacier Deep Archive'],
                    'correct': 3,
                    'explanation': 'S3 Glacier Deep Archive offers the lowest cost for long-term archival with retrieval times of 12+ hours.'
                }
            ]
        }
        return questions.get(concept_id, [])
    
    def _get_practical_exercise(self, concept_id: str) -> Dict[str, str]:
        """Get practical exercise for a concept"""
        exercises = {
            'ec2_basics': {
                'scenario': 'Your startup is experiencing rapid growth. Your single web server is struggling to handle the increasing traffic, especially during peak hours.',
                'task': 'Design an Auto Scaling solution that can handle traffic spikes automatically. Consider: minimum instances needed, maximum capacity, and scaling triggers.'
            },
            's3_storage': {
                'scenario': 'Your company generates large amounts of log data daily. Recent logs need quick access, but older logs are rarely accessed and storage costs are becoming expensive.',
                'task': 'Design an S3 lifecycle policy that automatically moves older data to cheaper storage classes while maintaining quick access to recent data.'
            }
        }
        return exercises.get(concept_id, {
            'scenario': 'You need to implement this AWS service in a real-world scenario.',
            'task': 'Think about how you would apply this concept in practice.'
        })
    
    def _get_key_takeaways(self, concept_id: str) -> List[str]:
        """Get key takeaways for a concept"""
        takeaways = {
            'ec2_basics': [
                "EC2 provides scalable virtual servers in the cloud",
                "Choose instance types based on your workload requirements",
                "Auto Scaling helps manage costs and performance automatically",
                "Security groups act as virtual firewalls for your instances"
            ],
            's3_storage': [
                "S3 provides virtually unlimited object storage",
                "Different storage classes optimize for access patterns and cost",
                "Lifecycle policies automate data management",
                "S3 offers 99.999999999% (11 9's) durability"
            ]
        }
        return takeaways.get(concept_id, ["Key concepts learned", "Practical applications understood"])
    
    def _get_max_options(self) -> int:
        """Get maximum number of options for current phase"""
        if self.current_phase == LearningPhase.QUIZ:
            questions = self._get_quiz_questions(self.current_concept.id)
            if self.current_page < len(questions):
                return len(questions[self.current_page]['options'])
        elif self.current_phase == LearningPhase.PRACTICAL:
            return 2  # Complete or Skip
        
        return 1
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_surface = self.font_small.render(test_line, True, (255, 255, 255))
            
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _render_simple_diagram(self, screen: pygame.Surface, x: int, y: int, diagram_type: str):
        """Render simple diagrams"""
        if diagram_type == 'auto_scaling_diagram':
            # Draw simple Auto Scaling diagram
            # Load Balancer
            pygame.draw.rect(screen, (100, 150, 255), (x, y, 80, 40))
            lb_text = self.font_small.render("Load Balancer", True, (255, 255, 255))
            screen.blit(lb_text, (x + 5, y + 12))
            
            # Instances
            for i in range(3):
                instance_x = x + 120 + (i * 90)
                pygame.draw.rect(screen, (50, 200, 50), (instance_x, y + 20, 60, 30))
                inst_text = self.font_small.render(f"EC2-{i+1}", True, (255, 255, 255))
                screen.blit(inst_text, (instance_x + 10, y + 27))
                
                # Arrow from LB to instances
                pygame.draw.line(screen, (255, 255, 255), (x + 80, y + 20), (instance_x, y + 35), 2)
            
            # Auto Scaling Group label
            asg_text = self.font_small.render("Auto Scaling Group", True, (255, 200, 100))
            screen.blit(asg_text, (x + 150, y + 70))
        
        elif diagram_type == 's3_lifecycle_diagram':
            # Draw S3 lifecycle diagram
            stages = ["Standard", "IA", "Glacier", "Deep Archive"]
            colors = [(100, 150, 255), (255, 200, 100), (150, 150, 255), (100, 100, 200)]
            
            for i, (stage, color) in enumerate(zip(stages, colors)):
                stage_x = x + (i * 100)
                pygame.draw.rect(screen, color, (stage_x, y, 80, 40))
                stage_text = self.font_small.render(stage, True, (255, 255, 255))
                screen.blit(stage_text, (stage_x + 5, y + 12))
                
                # Arrow to next stage
                if i < len(stages) - 1:
                    pygame.draw.line(screen, (255, 255, 255), (stage_x + 80, y + 20), (stage_x + 100, y + 20), 2)
                    # Arrow head
                    pygame.draw.polygon(screen, (255, 255, 255), [
                        (stage_x + 95, y + 15),
                        (stage_x + 95, y + 25),
                        (stage_x + 100, y + 20)
                    ])
            
            # Days labels
            days = ["0-30 days", "30-90 days", "90+ days"]
            for i, day_label in enumerate(days):
                day_x = x + 25 + (i * 100)
                day_text = self.font_small.render(day_label, True, (200, 200, 200))
                screen.blit(day_text, (day_x, y + 50))
    
    def get_completion_data(self) -> Dict:
        """Get completion data for progress tracking"""
        quiz_questions = self._get_quiz_questions(self.current_concept.id)
        quiz_percentage = (self.quiz_score / len(quiz_questions)) * 100 if quiz_questions else 0
        
        return {
            'concept_id': self.current_concept.id,
            'quiz_score': self.quiz_score,
            'quiz_total': len(quiz_questions),
            'quiz_percentage': quiz_percentage,
            'practical_completed': self.practical_completed,
            'passed': quiz_percentage >= 70 and self.practical_completed
        }