.. Shepherd Planning documentation master file, created by
   sphinx-quickstart on Fri Feb  2 12:21:15 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Shepherd's DevLog!
=============================================

.. toctree::
   :maxdepth: 2
   :caption: Overview

   00_overview/requirements_2020
   00_overview/feasibility_2020
   00_overview/concept_shepherd
   00_overview/concept_testbed
   00_overview/concept_tu_dresden
   00_overview/comparison_other_testbeds
   00_overview/learnings_other_testbeds

.. toctree::
   :maxdepth: 2
   :caption: Cape

   10_capes/concept_capes
   10_capes/concept_cad
   10_capes/cape_v20_design
   10_capes/cape_v21_design
   10_capes/cape_v21_performance
   10_capes/cape_v22_design
   10_capes/cape_v22_performance
   10_capes/test_for_functionality
   10_capes/cape_v23_design
   10_capes/cape_v23_performance
   10_capes/cape_v24_design
   10_capes/cape_v24_performance
   10_capes/cape_v24_measurements
   10_capes/cape_v25_design
   10_capes/cape_v26_design

   10_capes/harvesting_sources

.. toctree::
   :maxdepth: 2
   :caption: Targets

   20_targets/target_v23_design.md

.. toctree::
   :maxdepth: 2
   :caption: Components & Debugging

   30_components_debugging/beaglebone_boot_pins
   30_components_debugging/watchdog
   30_components_debugging/lsf_level_translator_v22/README
   30_components_debugging/noise_performance/README
   30_components_debugging/target_voltage
   30_components_debugging/recorder_drain
   30_components_debugging/cape_v24_emu_noise_improvements
   30_components_debugging/improve_pru

   30_components_debugging/harvester_validation_v23/README
   30_components_debugging/virtual_source_regulator/README


.. toctree::
   :maxdepth: 2
   :caption: Observer & Embedded Sys

   40_embedded_sys/concept_pru
   40_embedded_sys/concept_py

   40_embedded_sys/concept_casing.md

   40_embedded_sys/improve_linux
   40_embedded_sys/improve_security
   40_embedded_sys/improve_py_upgrade
   40_embedded_sys/fix_device_tree

   40_embedded_sys/crypto_module

   40_embedded_sys/evaluate_beaglebone_AI
   40_embedded_sys/evaluate_beaglebone_AI64
   40_embedded_sys/evaluate_raspberry_CM4


.. toctree::
   :maxdepth: 2
   :caption: Server

   60_server/requirements

   60_server/config_basics
   60_server/config_icmp
   60_server/config_rpc_portmapper
   60_server/config_sshd
   60_server/config_ssl_certificates

.. toctree::
   :maxdepth: 2
   :caption: Network

   70_network/requirements

.. toctree::
   :maxdepth: 2
   :caption: Web

   80_web/concept_web

.. toctree::
   :maxdepth: 2
   :caption: Student Projects

   90_student_projects/introduction
   90_student_projects/implement_dataviewer
   90_student_projects/improvement_for_memory_interface


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
