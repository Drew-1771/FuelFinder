//
//  ContentView.swift
//  project
//
//  Created by Drew S on 2/27/24.
//

import SwiftUI

extension Color {
    init(hex: UInt32) {
        let red = Double((hex & 0xFF0000) >> 16) / 255.0
        let green = Double((hex & 0x00FF00) >> 8) / 255.0
        let blue = Double(hex & 0x0000FF) / 255.0
        self.init(red: red, green: green, blue: blue)
    }
}

struct ContentView: View {
    var body: some View {
        MainTabView()
        }
    }

#Preview {
    ContentView()
}
